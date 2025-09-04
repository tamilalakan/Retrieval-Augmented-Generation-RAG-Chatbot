# RAG

A minimal Retrieval-Augmented Generation (RAG) example using LangChain, Chroma, and Google Vertex AI (Gemini and Embeddings) to answer questions over local documents (`.txt`, `.pdf`, `.docx`).

## Features

- Load and combine content from `data.txt`, `data.pdf`, and `data.docx`
- Split documents into overlapping chunks using `RecursiveCharacterTextSplitter`
- Create embeddings with `VertexAIEmbeddings` (`text-embedding-005`)
- Store vectors in a local Chroma DB (in-memory for this script)
- Query using `ChatVertexAI` (`gemini-2.0-flash-001`) via a simple RetrievalQA chain

## Prerequisites

- Python 3.9+ recommended
- A Google Cloud project with Vertex AI API enabled
- A Vertex AI service account key JSON (downloaded locally). This repo expects a file named `vertex_key.json` in the project root by default, but you can use any path via environment variable

## Setup

1) Clone and navigate into the project directory

```bash
cd RAG_Test_01
```

2) Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# CMD
.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate
```

3) Install dependencies

```bash
pip install -r requirements.txt
```

4) Configure environment

- Create a `.env` file in the project root with the path to your Google credentials JSON.
- On Windows, prefer an absolute path.

Example `.env`:

```env
GOOGLE_APPLICATION_CREDENTIALS=D:\\Projects\\RAG_Test_01\\vertex_key.json
```

If your key is elsewhere, set the value to that absolute path.

## Data files

Place your input files in the project root with the exact names used in the script:

- `data.txt`
- `data.pdf`
- `data.docx`

All three are optional individually, but the current script expects them to exist. If you remove one, update `main.py` accordingly.

## Run

```bash
python main.py
```

The script will:

- Load documents
- Chunk and embed them
- Build a Chroma vector store
- Run a sample query: "What This Package Provides"
- Print the generated answer

## How it works (high level)

- `langchain_community.document_loaders` loads text, PDF, and DOCX files
- `RecursiveCharacterTextSplitter` creates context-sized chunks
- `VertexAIEmbeddings` turns chunks into vector embeddings (`text-embedding-005`)
- `Chroma.from_texts` builds a temporary vector index
- `ChatVertexAI` (`gemini-2.0-flash-001`) answers the query using retrieved context via `RetrievalQA`

## Troubleshooting

- Authentication errors: Ensure `.env` points to a valid key and the service account has Vertex AI permissions.
- Import errors: Run `pip install -r requirements.txt` inside your activated virtual environment.
- File not found: Ensure `data.txt`, `data.pdf`, and `data.docx` exist or adjust `main.py` to skip missing loaders.
- API not enabled: In Google Cloud Console, enable Vertex AI API for your project.

## Project structure

```
RAG_Test_01/
├─ main.py
├─ requirements.txt
├─ vertex_key.json           # your service account key (do not commit)
├─ .env                      # your local env file (do not commit)
├─ data.txt | data.pdf | data.docx
└─ README.md
```

## Notes

- This example keeps the Chroma store in-memory for simplicity. For persistence, initialize Chroma with a `persist_directory` and call `persist()`.
- To change the demo question, edit the `query` variable in `main.py`.

## License

MIT
