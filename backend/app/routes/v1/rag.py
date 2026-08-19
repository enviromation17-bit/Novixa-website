from fastapi import APIRouter

from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


rag_service: RAGService | None = None


def get_rag_service() -> RAGService:
    global rag_service

    if rag_service is None:
        rag_service = RAGService()

    return rag_service


@router.post("/ingest")
def ingest_document(text: str) -> dict:
    service = get_rag_service()

    chunk_count = service.ingest_document(text)

    return {
        "success": True,
        "chunks_created": chunk_count,
    }


@router.get("/search")
def search_documents(
    query: str,
    top_k: int = 3,
) -> dict:
    service = get_rag_service()

    results = service.retrieve(
        query=query,
        top_k=top_k,
    )

    return {
        "query": query,
        "results": results,
    }