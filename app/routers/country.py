from fastapi import APIRouter, Query, HTTPException
from app.database import database
from app.models import country as country_model
from app.schemas import CountryOut, PaginatedResponse
from typing import Optional
from sqlalchemy import func, select

router = APIRouter()

@router.get("/countries", response_model=PaginatedResponse[CountryOut])
async def get_countries(
    page: int = Query(1, ge=1, description="Nomor halaman"),
    limit: int = Query(10, le=100, description="Jumlah item per halaman"),
    regionid: Optional[int] = Query(None, description="Filter berdasarkan ID Wilayah"),
    sort_by: str = Query("countryid", description="Urutkan berdasarkan field"),
    order: str = Query("asc", description="Urutan (asc/desc)")
):
    offset = (page - 1) * limit
    query = country_model.select()
    count_query = select(func.count()).select_from(country_model)

    if regionid is not None:
        query = query.where(country_model.c.regionid == regionid)
        count_query = count_query.where(country_model.c.regionid == regionid)

    total_items = await database.fetch_val(count_query)
    total_pages = (total_items + limit - 1) // limit

    allowed_sort_fields = {column.name for column in country_model.c}
    if sort_by not in allowed_sort_fields:
        sort_by = "countryid"

    sort_column = country_model.c[sort_by]
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    query = query.offset(offset).limit(limit)
    results = await database.fetch_all(query)

    return PaginatedResponse(
        status="success",
        message="Countries fetched successfully.",
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        data=results
    )

@router.get("/countries/{country_id}", response_model=CountryOut)
async def get_country(country_id: int):
    query = country_model.select().where(country_model.c.countryid == country_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Country with id {country_id} not found")
    return result