# DocQA-RAG

A simple Document Q&A system built with **FastAPI**, **LangChain**, **Chroma**, **Groq**, and **HuggingFace embeddings**.

The system allows users to:

* Upload PDF or TXT files
* Split documents into chunks
* Create embeddings and store them in Chroma
* Ask questions about the uploaded document
* Get answers based only on the document content (with source citations)

## RAG Pipeline

```
Upload → Split → Embeddings (HuggingFace) → Chroma → Retrieve → LLM (Groq) → Answer
```

## Main Components

* `main.py` – app entry point
* `config.py` – project settings
* `schemas.py` – request/response models
* `file_controller.py` – file handling
* `rag_pipeline.py` – loading, splitting, embeddings and Q&A
* `routes/qa.py` – API endpoints

## API

```
POST /api/v1/upload/{project_id}
POST /api/v1/process/{project_id}
POST /api/v1/ask/{project_id}
```

## How to Run

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your free Groq API key (get one at [console.groq.com](https://console.groq.com)):

```
GROQ_API_KEY=your_groq_api_key
```

Then run:

```bash
uvicorn main:app --reload
```

Open Swagger API documentation:

```
http://127.0.0.1:8000/docs
```

## Notes

* The embedding model (`sentence-transformers`, multilingual) runs **fully locally and free** — no API key or cost involved. It downloads automatically on first use.
* The LLM (Groq) is **free tier**, no credit card required.
* The project uses LCEL (LangChain Expression Language) to build the RAG chain, and returns the answer along with the retrieved source chunks.
* The prompt explicitly instructs the model to answer only from the retrieved context, and to say so clearly if the information isn't found — this prevents hallucination.

## Technologies

Python • FastAPI • LangChain • Chroma • Groq • HuggingFace (sentence-transformers) • Pydantic
