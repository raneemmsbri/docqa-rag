import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    

    APP_NAME: str = "myproject-rag"
    APP_VERSION: str = "0.1"

    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    LLM_MODEL_NAME: str = "openai/gpt-oss-20b"
    FILE_ALLOWED_TYPES: list = ["application/pdf", "text/plain"]
    FILE_MAX_SIZE_MB: int = 10

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    RETRIEVAL_TOP_K: int = 3

    UPLOAD_DIR: str = "uploads"
    CHROMA_DIR: str = "chroma_db"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
    )


def get_settings() :
    return Settings()

        
    
    
    
    
    
    


    


