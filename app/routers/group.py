from fastapi import APIRouter, Query, HTTPException
from app.database import database
from app.models import group as group_model
from app.schemas import GroupOut, PaginatedResponse
from typing import Optional
from sqlalchemy import func, select

router = APIRouter()

@router.get("/groups", response_model=PaginatedResponse[GroupOut])
async def get_groups(
    page: int = Query(1, ge=1, description="Nomor halaman"),
    limit: int = Query(10, le=100, description="Jumlah item per halaman"),
    gname: Optional[str] = Query(None, description="Filter berdasarkan Nama Grup"),
    sort_by: str = Query("gid", description="Urutkan berdasarkan field"),
    order: str = Query("asc", description="Urutan (asc/desc)")
):
    offset = (page - 1) * limit
    query = group_model.select()
    count_query = select(func.count()).select_from(group_model)

    if gname is not None:
        query = query.where(func.lower(group_model.c.gname).like(f"%{gname.lower()}%"))
        count_query = count_query.where(func.lower(group_model.c.gname).like(f"%{gname.lower()}%"))

    total_items = await database.fetch_val(count_query)
    total_pages = (total_items + limit - 1) // limit

    allowed_sort_fields = {column.name for column in group_model.c}
    if sort_by not in allowed_sort_fields:
        sort_by = "gid"

    sort_column = group_model.c[sort_by]
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    query = query.offset(offset).limit(limit)
    results = await database.fetch_all(query)

    return PaginatedResponse(
        status="success",
        message="Groups fetched successfully.",
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        data=results
    )

@router.get("/groups/{group_id}", response_model=GroupOut)
async def get_group(group_id: int):
    query = group_model.select().where(group_model.c.gid == group_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Group with id {group_id} not found")
    return result