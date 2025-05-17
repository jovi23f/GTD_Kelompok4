from fastapi import APIRouter, Query, HTTPException
from app.database import database
from app.models import attack as attack_model
from app.schemas import AttackOut, PaginatedResponse
from typing import Optional
from sqlalchemy import func, select

router = APIRouter()

@router.get("/attacks", response_model=PaginatedResponse[AttackOut])
async def get_attacks(
    page: int = Query(1, ge=1, description="Nomor halaman"),
    limit: int = Query(10, le=100, description="Jumlah item per halaman"),
    attacktype: Optional[str] = Query(None, description="Filter berdasarkan Tipe Serangan"),
    sort_by: str = Query("attackid", description="Urutkan berdasarkan field"),
    order: str = Query("asc", description="Urutan (asc/desc)")
):
    offset = (page - 1) * limit
    query = attack_model.select()
    count_query = select(func.count()).select_from(attack_model)

    if attacktype is not None:
        query = query.where(func.lower(attack_model.c.attacktype).like(f"%{attacktype.lower()}%"))
        count_query = count_query.where(func.lower(attack_model.c.attacktype).like(f"%{attacktype.lower()}%"))

    total_items = await database.fetch_val(count_query)
    total_pages = (total_items + limit - 1) // limit

    allowed_sort_fields = {column.name for column in attack_model.c}
    if sort_by not in allowed_sort_fields:
        sort_by = "attackid"

    sort_column = attack_model.c[sort_by]
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    query = query.offset(offset).limit(limit)
    results = await database.fetch_all(query)

    return PaginatedResponse(
        status="success",
        message="Attacks fetched successfully.",
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        data=results
    )

@router.get("/attacks/{attack_id}", response_model=AttackOut)
async def get_attack(attack_id: int):
    query = attack_model.select().where(attack_model.c.attackid == attack_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Attack with id {attack_id} not found")
    return result