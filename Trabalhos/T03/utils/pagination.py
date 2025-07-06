from fastapi import Query

def get_pagination(
    page: int = Query(1, ge=1, description="Página atual"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade por página")
):
    return {"page": page, "limit": limit}
