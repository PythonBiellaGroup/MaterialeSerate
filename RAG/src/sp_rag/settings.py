from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DENSE_EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    SPARSE_EMBEDDING_MODEL: str = "Qdrant/bm25"

    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 32

    CHAT_MODEL: str = "openai:gpt-4o-mini"
    # CHAT_MODEL: str = "ollama:llama3.2"
    CHAT_MODEL_KWARGS: dict = {"model": CHAT_MODEL, "temperature": 0}


settings = Settings()
