import os
import shutil

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
from starlette import status

from config import get_settings, Settings
from schemas import (
    UploadResponse,
    ProcessRequest,
    ProcessResponse,
    QuestionRequest,
    AnswerResponse,
    SourceChunk,
)
from enums import ResponseSignal
import file_controller
import rag_pipeline 


qa_router = APIRouter(prefix="/api/v1", tags=["qa"])


@qa_router.post("/upload/{project_id}", response_model=UploadResponse)
async def upload_file(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings),
):
    is_valid, signal = file_controller.validate_uploaded_file(file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": signal},
        )

    file_path, file_id = file_controller.generate_unique_filepath(
        orig_file_name=file.filename, project_id=project_id
    )

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value},
        )

    return UploadResponse(
        signal=ResponseSignal.FILE_UPLOAD_SUCCESS.value,
        file_id=file_id,
        project_id=project_id,
    ) 


@qa_router.post("/process/{project_id}", response_model=ProcessResponse)
async def process_file(project_id: str, request: ProcessRequest):
    file_path = file_controller.find_file_path(
        file_id=request.file_id, project_id=project_id
    )

    if not os.path.exists(file_path):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"signal": ResponseSignal.FILE_NOT_FOUND.value},
        )

    try:
        documents = rag_pipeline.load_document(file_path)
        chunks = rag_pipeline.split_document(
            documents,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
        # نستخدم file_id كمعرف فريد للـ vectorstore بتاع الملف ده
        rag_pipeline.build_vectorstore(file_id=request.file_id, chunks=chunks)

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.PROCESSING_FAILED.value,
                "error": str(e),
            },
        )

    return ProcessResponse(
        signal=ResponseSignal.PROCESSING_SUCCESS.value,
        chunks_count=len(chunks),
    )


@qa_router.post("/ask/{project_id}", response_model=AnswerResponse)
async def ask_question(project_id: str, request: QuestionRequest):
    if not request.file_id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_NOT_FOUND.value},
        )

    answer_text, source_docs, found_relevant_info = rag_pipeline.answer_question(
        file_id=request.file_id,
        question=request.question,
        top_k=request.top_k,
    )

    if answer_text is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_NOT_PROCESSED_YET.value},
        )

    sources = [
        SourceChunk(
            file_id=request.file_id,
            page=doc.metadata.get("page"),
            content_snippet=doc.page_content[:200],
        )
        for doc in source_docs
    ]

    return AnswerResponse(
        answer=answer_text,
        sources=sources,
        found_relevant_info=found_relevant_info,
    )
