from fastapi import APIRouter, Query, HTTPException
from app.database import database
from app.models import target as target_model
from app.schemas import TargetOut, PaginatedResponse
from typing import Optional
from sqlalchemy import func, select

router = APIRouter()

@router.get("/targets", response_model=PaginatedResponse[TargetOut])
async def get_targets(
    page: int = Query(1, ge=1, description="Nomor halaman"),
    limit: int = Query(10, le=100, description="Jumlah item per halaman"),
    targtype1_txt: Optional[str] = Query(None, description="Filter berdasarkan Tipe Target 1"),
    countryid: Optional[int] = Query(None, description="Filter berdasarkan ID Negara"),
    regionid: Optional[int] = Query(None, description="Filter berdasarkan ID Wilayah"),
    sort_by: str = Query("targetid", description="Urutkan berdasarkan field"),
    order: str = Query("asc", description="Urutan (asc/desc)")
):
    offset = (page - 1) * limit
    query = target_model.select()
    count_query = select(func.count()).select_from(target_model)

    if targtype1_txt is not None:
        query = query.where(func.lower(target_model.c.targtype1_txt).like(f"%{targtype1_txt.lower()}%"))
        count_query = count_query.where(func.lower(target_model.c.targtype1_txt).like(f"%{targtype1_txt.lower()}%"))
    if countryid is not None:
        query = query.where(target_model.c.countryid == countryid)
        count_query = count_query.where(target_model.c.countryid == countryid)
    if regionid is not None:
        query = query.where(target_model.c.regionid == regionid)
        count_query = count_query.where(target_model.c.regionid == regionid)

    total_items = await database.fetch_val(count_query)
    total_pages = (total_items + limit - 1) // limit

    allowed_sort_fields = {column.name for column in target_model.c}
    if sort_by not in allowed_sort_fields:
        sort_by = "targetid"

    sort_column = target_model.c[sort_by]
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    query = query.offset(offset).limit(limit)
    results = await database.fetch_all(query)

    return PaginatedResponse(
        status="success",
        message="Targets fetched successfully.",
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        data=results
    )

@router.get("/targets/{target_id}", response_model=TargetOut)
async def get_target(target_id: int):
    query = target_model.select().where(target_model.c.targetid == target_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Target with id {target_id} not found")
    return result