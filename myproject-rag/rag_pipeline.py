



import os
from typing import List, Optional, Tuple

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from config import get_settings

settings = get_settings()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def load_document(file_path: str) -> List[Document]:
    file_ext = os.path.splitext(file_path)[-1].lower()

    if file_ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"نوع الملف {file_ext} غير مدعوم")

    return loader.load()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def split_document(
    documents: List[Document],
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or settings.CHUNK_SIZE,
        chunk_overlap=chunk_overlap or settings.CHUNK_OVERLAP,
        length_function=len,
    )
    return splitter.split_documents(documents)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_vectorstore_path(file_id: str) -> str:
    return os.path.join(settings.CHROMA_DIR, file_id)


def _get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME) 

def build_vectorstore(file_id: str, chunks: List[Document]) -> Chroma:
    persist_path = get_vectorstore_path(file_id)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=_get_embeddings(),
        persist_directory=persist_path,
    )
    return vectorstore


def load_vectorstore(file_id: str) -> Optional[Chroma]:
    persist_path = get_vectorstore_path(file_id)

    if not os.path.exists(persist_path):
        return None

    return Chroma(
        persist_directory=persist_path,
        embedding_function=_get_embeddings(),
    )
    


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
QA_PROMPT_TEMPLATE = """أنت مساعد بيجاوب على أسئلة بناءً على المستندات المرفوعة فقط.
استخدم المعلومات الموجودة في السياق التالي فقط للإجابة.
لو المعلومة مش موجودة في السياق، قول بوضوح بالظبط الجملة دي: "مفيش معلومة عن ده في المستند المرفوع"، من غير ما تخترع إجابة.

السياق:
{context}

السؤال: {question}

الإجابة:"""

QA_PROMPT = PromptTemplate(
    template=QA_PROMPT_TEMPLATE,
    input_variables=["context", "question"],
)


def _format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def answer_question(
    file_id: str, question: str, top_k: int = None
) -> Tuple[Optional[str], List[Document], bool]:
    vectorstore = load_vectorstore(file_id)

    if vectorstore is None:
        return None, [], False

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": top_k or settings.RETRIEVAL_TOP_K}
    )

    retrieved_docs = retriever.invoke(question)

    llm = ChatGroq(
        model=settings.LLM_MODEL_NAME,
        temperature=0,
        groq_api_key=settings.GROQ_API_KEY,
    )
    
    
    chain = QA_PROMPT | llm | StrOutputParser()

    answer_text = chain.invoke(
        {
            "context": _format_docs(retrieved_docs),
            "question": question,
        }
    )

    found_relevant_info = (
        "مفيش معلومة" not in answer_text and len(retrieved_docs) > 0
    )

    return answer_text, retrieved_docs, found_relevant_info
