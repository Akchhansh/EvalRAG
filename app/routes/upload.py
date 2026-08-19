from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from app.services.pdf_services import extract_text_from_pdf
from app.services.chunk_services import chunk_text
from app.services.embedding_services import generate_embeddings
from app.services.qdrant_services import store_embeddings

router= APIRouter()

UPLOAD_DIR= Path("data/uploads")
PROCESSED_DIR= Path("data/processed")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 
PROCESSED_DIR.mkdir(parents=True, exist_ok=True) 

@router.post("/upload")
async def upload_pdf(file: UploadFile= File(...)):
    #Upload
    file_path= UPLOAD_DIR/file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #Extract text
    text= extract_text_from_pdf(str(file_path))
    # output_file= PROCESSED_DIR/f"{file.filename}.txt"

    # with open(output_file, "w", encoding="utf-8") as f:
    #     f.write(text)

    #Chunking
    chunks=chunk_text(text)
    for i,chunk in enumerate(chunks):
        chunk_file=PROCESSED_DIR/F"{file.filename}_chunk_{i}.txt"
        with open(chunk_file, "w", encoding="utf-8") as f:
            f.write(chunk)
    embeddings = generate_embeddings(chunks)
    store_embeddings(
        chunks,
        embeddings,
        file.filename
        )
    return{
        "message":"PDF processed successfully sucessfully",
        "filename":file.filename,
        "chunks":len(chunks),
        "vector_stored":len(embeddings)
    }