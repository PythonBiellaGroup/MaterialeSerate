from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage

from sp_rag.core.retrievers import RetrievalStrategy
from sp_rag.rag import AgenticRAG
from sp_rag.vectordb.qdrant import QdrantVectorDB

st.set_page_config(page_title="Scientific Paper Assistant", layout="wide")
st.title("🧪 Scientific Paper Assistant")

# -- INIT & RESET BUTTON --
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "rag_pipeline" not in st.session_state:
    vs = QdrantVectorDB(
        url="http://localhost:6333", collection="arxiv_papers"
    ).vector_store
    st.session_state.rag_pipeline = AgenticRAG(
        vs, retrieval_strategy=RetrievalStrategy.SIMPLE
    )

# Sidebar clear/reset
if st.sidebar.button("🧹 Clear Chat & Reset Agent"):
    st.session_state.chat_history = []
    vs = QdrantVectorDB(
        url="http://localhost:6333", collection="arxiv_papers"
    ).vector_store
    st.session_state.rag_pipeline = AgenticRAG(
        vs, retrieval_strategy=RetrievalStrategy.SIMPLE
    )
    st.success("✅ Chat cleared and Agent reset.")

rag = st.session_state.rag_pipeline

# -- LAYOUT --
col_chat, col_memory = st.columns([2, 1])

# -- RIGHT PANEL: AGENT MEMORY --
with col_memory:
    st.subheader("🧠 Agent Memory")

    memory_msgs = rag.get_memory_messages()
    if memory_msgs:
        with st.expander("🗂 Full Memory State", expanded=False):
            for msg in memory_msgs:
                role = "🧑‍🔬 User" if isinstance(msg, HumanMessage) else "🤖 Assistant"
                st.markdown(f"**{role}**: {msg.content}")

# -- LEFT PANEL: CHAT UI --
with col_chat:
    st.subheader("💬 Chat with the Assistant")

    # Display existing chat history
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp")
        icon = "🧑‍🔬" if role == "user" else "🤖"
        ts_str = f"_{timestamp.strftime('%H:%M:%S')}_ " if timestamp else ""

        with st.chat_message(role):
            st.markdown(f"{icon} {ts_str}  \n{content}")

prompt = st.chat_input("Ask a question about scientific papers")

if prompt:
    now = datetime.now()
    st.session_state.chat_history.append(
        {"role": "user", "content": prompt, "timestamp": now}
    )

    # Render user message
    with st.chat_message("user"):
        st.markdown(f"_{now.strftime('%H:%M:%S')}_  \n{prompt}")

    # Get response from agent
    with st.chat_message("assistant"):
        response = rag.invoke(prompt)
        st.markdown(f"_{datetime.now().strftime('%H:%M:%S')}_  \n{response}")

    # Store assistant message
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response, "timestamp": datetime.now()}
    )
