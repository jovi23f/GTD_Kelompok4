from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import region as region_model
from app.schemas import RegionOut, PaginatedResponse
from sqlalchemy import select, func

router = APIRouter()

@router.get("/regions", response_model=PaginatedResponse[RegionOut])
async def get_regions():
    query = select(region_model)
    results = await database.fetch_all(query)
    total_items = await database.fetch_val(select(func.count()).select_from(region_model))
    return PaginatedResponse(
        status="success",
        message="Regions fetched successfully.",
        page=1,
        total_pages=1, # Karena tidak ada limit, anggap 1 halaman
        total_items=total_items,
        data=results
    )

@router.get("/regions/{region_id}", response_model=RegionOut)
async def get_region(region_id: int):
    query = select(region_model).where(region_model.c.regionid == region_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail=f"Region with id {region_id} not found")
    return result