from pydantic import BaseModel, Field
from typing import List, Optional


class UploadResponse(BaseModel):
    
    signal: str
    file_id: str
    project_id: str


class ProcessRequest(BaseModel):
    
    file_id: str
    chunk_size: Optional[int] = 500
    chunk_overlap: Optional[int] = 50


class ProcessResponse(BaseModel):
    signal: str
    chunks_count: int


class QuestionRequest(BaseModel):
    
    question: str = Field(..., min_length=3, description="the question ")
    file_id: Optional[str] = Field(
        None, description="file id that will search on it "
    )
    top_k: Optional[int] = Field(3, description="number of chuncks will retrive")


class SourceChunk(BaseModel):
    file_id: str
    page: Optional[int] = None
    content_snippet: str


class AnswerResponse(BaseModel):
    
    answer: str
    sources: List[SourceChunk]
    found_relevant_info: bool
