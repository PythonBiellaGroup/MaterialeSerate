import uuid

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    RemoveMessage,
    SystemMessage,
)
from langchain_core.tools import create_retriever_tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import create_react_agent
from loguru import logger

from sp_rag import settings
from sp_rag.core.retrievers import RetrieverFactory

from .base import BaseRAG


class AgenticRAG(BaseRAG):
    """
    An agentic Retrieval-Augmented Generation pipeline utilizing a ReAct agent.
    """

    def __init__(self, vectorstore, retrieval_strategy):
        logger.info("Initializing AgenticRAG...")

        self.retriever = RetrieverFactory.get_retriever(retrieval_strategy, vectorstore)
        self.retriever_tool = create_retriever_tool(
            retriever=self.retriever,
            name="retriever",
            description=(
                "Search a curated collection of scientific papers from arXiv, focused on categories: cs.AI, cs.CL, and cs.CV. "
                "The corpus includes papers published since September 2024 and filtered by keywords like "
                "'Retrieval-Augmented Generation (RAG)', 'image classification', 'computer vision', and 'semantic segmentation'. "
                "Use this tool to look up recent research findings, methods, benchmarks, and terminology from state-of-the-art publications."
            ),
        )

        self.tools = [self.retriever_tool]
        self.llm = init_chat_model(**settings.CHAT_MODEL_KWARGS)
        self.agent_model = self.llm.bind_tools(self.tools)

        self.agent_executor = self._create_agent()

        self.memory = MemorySaver()
        self._thread_id = str(uuid.uuid4())

        self.summary_prompt = HumanMessage(
            content="Summarize the above conversation into a single, coherent message that captures key technical insights, terminology, and context. "
            "Preserve specific methods, findings, or questions discussed, and avoid generalizations. "
            "The summary should be suitable for use as background context in future scientific queries."
        )

        self.agent_sys_prompt = SystemMessage(
            content="You are a helpful AI assistant designed to answer questions about scientific papers using a Retrieval-Augmented Generation (RAG) system based on arXiv data."
            "Think step-by-step before answering."
            "Use available tools for retrieval when necessary."
            "For complex, technical, or multi-part questions, break them down into smaller subquestions or rephrase them from different angles to ensure thorough coverage."
            "Generate diverse subqueries that target different formulations, perspectives, or terminology used in scientific literature."
            "Examples include: simplifying technical language, using synonyms, focusing on methods vs. results, or isolating specific variables or assumptions."
            "Before presenting your final answer, briefly summarize the steps you took, including how you phrased subqueries and why, and whether any tools were used."
        )

        self.graph = self._build_graph()

    def _create_agent(self):
        def _react_prompt(state: MessagesState):

            return [self.agent_sys_prompt] + state["messages"]

        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=_react_prompt,
        )

    def memory_update(self, state: MessagesState):
        logger.info("Running summarization node...")
        messages: list[AnyMessage] = state["messages"]

        if len(messages) < 5:
            return {}

        last_user_msg = messages[-1]
        summary = self.llm.invoke(messages[:-1] + [self.summary_prompt])
        remove = [RemoveMessage(id=m.id) for m in messages[:-1]]  # type: ignore
        return {"messages": [summary, *remove, last_user_msg]}

    def _build_graph(self):
        workflow = StateGraph(MessagesState)
        workflow.set_entry_point("agent")

        workflow.add_node("agent", self.agent_executor)
        workflow.add_node("memory_update", self.memory_update)

        workflow.add_edge("agent", "memory_update")
        workflow.add_edge("memory_update", END)

        return workflow.compile(checkpointer=self.memory)

    def invoke(self, user_input: str) -> str:
        logger.info(f"Invoking AgenticRAG pipeline with question: {user_input}")

        state = self.graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": self._thread_id}},
        )

        final_message = state["messages"][-1]
        return getattr(final_message, "content", str(final_message))

    def get_memory_messages(self) -> list[AnyMessage]:
        """Return the current message history from memory for UI display."""
        state = self.graph.get_state({"configurable": {"thread_id": self._thread_id}})

        return state.values.get("messages", [])
