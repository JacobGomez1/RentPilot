from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/search")
def search_apartments(query: str = Query(None)):
    return {
        "query": query,
        "results": []
    }