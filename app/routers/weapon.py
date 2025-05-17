from fastapi import APIRouter, Query, HTTPException
from app.database import database
from app.models import weapon as weapon_model
from app.schemas import WeaponOut, PaginatedResponse
from typing import Optional
from sqlalchemy import func, select

router = APIRouter()

@router.get("/weapons", response_model=PaginatedResponse[WeaponOut])
async def get_weapons(
    page: int = Query(1, ge=1, description="Nomor halaman"),
    limit: int = Query(10, le=100, description="Jumlah item per halaman"),
    weaptype1_txt: Optional[str] = Query(None, description="Filter berdasarkan Tipe Senjata 1"),
    sort_by: str = Query("weaponid", description="Urutkan berdasarkan field"),
    order: str = Query("asc", description="Urutan (asc/desc)")
):
    offset = (page - 1) * limit
    query = weapon_model.select()
    count_query = select(func.count()).select_from(weapon_model)

    if weaptype1_txt is not None:
        query = query.where(func.lower(weapon_model.c.weaptype1_txt).like(f"%{weaptype1_txt.lower()}%"))
        count_query = count_query.where(func.lower(weapon_model.c.weaptype1_txt).like(f"%{weaptype1_txt.lower()}%"))

    total_items = await database.fetch_val(count_query)
    total_pages = (total_items + limit - 1) // limit

    allowed_sort_fields = {column.name for column in weapon_model.c}
    if sort_by not in allowed_sort_fields:
        sort_by = "weaponid"

    sort_column = weapon_model.c[sort_by]
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    query = query.offset(offset).limit(limit)
    results = await database.fetch_all(query)

    return PaginatedResponse(
        status="success",
        message="Weapons fetched successfully.",
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        data=results
    )

@router.get("/weapons/{weapon_id}", response_model=WeaponOut)
async def get_weapon(weapon_id: int):
    query = weapon_model.select().where(weapon_model.c.weaponid == weapon_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Weapon with id {weapon_id} not found")
    return result