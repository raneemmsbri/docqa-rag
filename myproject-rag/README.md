# DocQA-RAG

A simple Document Q&A system built with **FastAPI, LangChain, Chroma, and OpenAI**.

The system allows users to:

* Upload PDF or TXT files
* Split documents into chunks
* Create embeddings and store them in Chroma
* Ask questions about the uploaded document
* Get answers based only on the document content

### RAG Pipeline

**Upload → Split → Embeddings → Chroma → Retrieve → LLM → Answer**

### Main Components

* `main.py` – app entry point
* `config.py` – project settings
* `schemas.py` – request/response models
* `file_controller.py` – file handling
* `rag_pipeline.py` – loading, splitting, embeddings and Q&A
* `routes/qa.py` – API endpoints

### API

```text
POST /api/v1/upload/{project_id}
POST /api/v1/process/{project_id}
POST /api/v1/ask/{project_id}
```

### How to Run

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_api_key
```

Then run:

```bash
uvicorn src.main:app --reload --port 8001
```

Open Swagger API documentation:

```text
http://127.0.0.1:8001/docs
```

The project uses **LCEL** to build the RAG chain and returns the answer with the retrieved sources.

### Technologies

Python • FastAPI • LangChain • Chroma • OpenAI • Pydantic
