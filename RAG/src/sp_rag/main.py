from sp_rag.core.retrievers import RetrievalStrategy
from sp_rag.rag import AgenticRAG
from sp_rag.vectordb.qdrant import QdrantVectorDB

if __name__ == "__main__":
    vs = QdrantVectorDB(
        url="http://localhost:6333", collection="arxiv_papers"
    ).vector_store

    rag = AgenticRAG(vs, retrieval_strategy=RetrievalStrategy.SIMPLE)

    rag.print_graph()
    response = rag.invoke(
        "What are the methods for benchmarking LLM-based agents and what applications are agents used in."
    )
    print(response)

    response = rag.invoke(
        "Can you find common trends and translate the output in italian?"
    )
    print(response)
