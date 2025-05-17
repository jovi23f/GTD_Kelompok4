from fastapi import APIRouter, Query, HTTPException, Request, Depends
from app.database import database
from app.models import event as event_model, region as region_model, group as group_model, weapon as weapon_model, target as target_model, country as country_model, attack as attack_model
from app.schemas import EventOut, PaginatedResponse, EventQueryParams, EventPathParams  # Import model Pydantic
from typing import Optional, List, Dict, Any
from sqlalchemy import func, select, join
import math

router = APIRouter()

def replace_nan_with_none(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Mengganti nilai NaN dalam dictionary dengan None.
    """
    processed_data = []
    for row in data:
        new_row = {}
        for key, value in row.items():
            if isinstance(value, float) and math.isnan(value):
                new_row[key] = None
            else:
                new_row[key] = value
        processed_data.append(new_row)
    return processed_data

@router.get("/events", response_model=PaginatedResponse[EventOut])
async def get_events(
    request: Request,
    query_params: EventQueryParams = Depends()
):
    expected_params = {
        "page", "limit", "iyear", "imonth", "iday", "location", "crit1", "crit2", "crit3",
        "targetid", "gid", "weaponid", "attackid", "regionid", "region_name", "countryid",
        "group_name", "weapon_type", "target_name", "country_name", "attacktype", "sort_by", "order"
    }
    provided_params = set(request.query_params.keys())
    unexpected_params = provided_params - expected_params

    if unexpected_params:
        raise HTTPException(
            status_code=400,
            detail=f"Parameter query tidak valid: {', '.join(unexpected_params)}"
        )
    page = query_params.page
    limit = query_params.limit
    iyear = query_params.iyear
    imonth = query_params.imonth
    iday = query_params.iday
    location = query_params.location
    crit1 = query_params.crit1
    crit2 = query_params.crit2
    crit3 = query_params.crit3
    targetid = query_params.targetid
    gid = query_params.gid
    weaponid = query_params.weaponid
    attackid = query_params.attackid
    regionid = query_params.regionid
    region_name = query_params.region_name
    countryid = query_params.countryid
    group_name = query_params.group_name
    weapon_type = query_params.weapon_type
    target_name = query_params.target_name
    country_name = query_params.country_name
    attacktype = query_params.attacktype
    sort_by = query_params.sort_by
    order = query_params.order

    try:
        offset = (page - 1) * limit
        # Lakukan JOIN antara tabel event dan tabel terkait
        join_stmt = join(event_model, region_model, event_model.c.regionid == region_model.c.regionid, isouter=True)
        join_stmt = join(join_stmt, group_model, event_model.c.gid == group_model.c.gid, isouter=True)
        join_stmt = join(join_stmt, weapon_model, event_model.c.weaponid == weapon_model.c.weaponid, isouter=True)
        join_stmt = join(join_stmt, target_model, event_model.c.targetid == target_model.c.targetid, isouter=True)
        join_stmt = join(join_stmt, country_model, event_model.c.countryid == country_model.c.countryid, isouter=True)
        join_stmt = join(join_stmt, attack_model, event_model.c.attackid == attack_model.c.attackid, isouter=True)

        query = select(event_model).select_from(join_stmt)
        count_query = select(func.count()).select_from(join_stmt)

        # Filter
        if iyear is not None:
            query = query.where(event_model.c.iyear == iyear)
            count_query = count_query.where(event_model.c.iyear == iyear)
        if imonth is not None:
            query = query.where(event_model.c.imonth == imonth)
            count_query = count_query.where(event_model.c.imonth == imonth)
        if iday is not None:
            query = query.where(event_model.c.iday == iday)
            count_query = count_query.where(event_model.c.iday == iday)
        if location is not None:
            query = query.where(func.lower(event_model.c.location).like(f"%{location.lower()}%"))
            count_query = count_query.where(func.lower(event_model.c.location).like(f"%{location.lower()}%"))
        if crit1 is not None:
            query = query.where(event_model.c.crit1 == crit1)
            count_query = count_query.where(event_model.c.crit1 == crit1)
        if crit2 is not None:
            query = query.where(event_model.c.crit2 == crit2)
            count_query = count_query.where(event_model.c.crit2 == crit2)
        if crit3 is not None:
            query = query.where(event_model.c.crit3 == crit3)
            count_query = count_query.where(event_model.c.crit3 == crit3)
        if targetid is not None:
            query = query.where(event_model.c.targetid == targetid)
            count_query = count_query.where(event_model.c.targetid == targetid)
        if gid is not None:
            query = query.where(event_model.c.gid == gid)
            count_query = count_query.where(event_model.c.gid == gid)
        if weaponid is not None:
            query = query.where(event_model.c.weaponid == weaponid)
            count_query = count_query.where(event_model.c.weaponid == weaponid)
        if attackid is not None:
            query = query.where(event_model.c.attackid == attackid)
            count_query = count_query.where(event_model.c.attackid == attackid)
        if regionid is not None:
            query = query.where(event_model.c.regionid == regionid)
            count_query = count_query.where(event_model.c.regionid == regionid)
        if countryid is not None:
            query = query.where(event_model.c.countryid == countryid)
            count_query = count_query.where(event_model.c.countryid == countryid)
        # Filter berdasarkan nama region
        if region_name is not None:
            query = query.where(func.lower(region_model.c.region).like(f"%{region_name.lower()}%"))
            count_query = count_query.where(func.lower(region_model.c.region).like(f"%{region_name.lower()}%"))
        if group_name is not None:
            query = query.where(func.lower(group_model.c.gname).like(f"%{group_name.lower()}%"))
            count_query = count_query.where(func.lower(group_model.c.gname).like(f"%{group_name.lower()}%"))

        if weapon_type is not None:
            query = query.where(func.lower(weapon_model.c.weaptype1_txt).like(f"%{weapon_type.lower()}%"))
            count_query = count_query.where(func.lower(weapon_model.c.weaptype1_txt).like(f"%{weapon_type.lower()}%"))

        if target_name is not None:
            query = query.where(func.lower(target_model.c.target1).like(f"%{target_name.lower()}%"))
            count_query = count_query.where(func.lower(target_model.c.target1).like(f"%{target_name.lower()}%"))

        if country_name is not None:
            query = query.where(func.lower(country_model.c.country).like(f"%{country_name.lower()}%"))
            count_query = count_query.where(func.lower(country_model.c.country).like(f"%{country_name.lower()}%"))

        if attacktype is not None:
            query = query.where(func.lower(attack_model.c.attacktype).like(f"%{attacktype.lower()}%"))
            count_query = count_query.where(func.lower(attack_model.c.attacktype).like(f"%{attacktype.lower()}%"))

        total_items = await database.fetch_val(count_query)
        total_pages = (total_items + limit - 1) // limit

        allowed_sort_fields = {column.name for column in event_model.c}
        if sort_by not in allowed_sort_fields:
            sort_by = "eventid"  # Default sort tetap eventid

        sort_column = event_model.c[sort_by]
        if order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        query = query.offset(offset).limit(limit)
        results = await database.fetch_all(query)
        # Replace NaN values with None
        processed_results = replace_nan_with_none( [dict(row) for row in results] )

        return PaginatedResponse(
            status="success",
            message="Events fetched successfully.",
            page=page,
            total_pages=total_pages,
            total_items=total_items,
            data=[EventOut(**item) for item in processed_results]
        )
    except Exception as e:
        print(f"Terjadi kesalahan internal saat memproses /events: {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal pada server.")

@router.get("/events/{event_id}", response_model=EventOut)
async def get_event(path_params: EventPathParams = Depends()):
    event_id = path_params.event_id
    try:
        query = select(event_model).where(event_model.c.eventid == event_id)
        result = await database.fetch_one(query)
        if not result:
            raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
        result_dict = dict(result)
        result_dict = replace_nan_with_none([result_dict])[0]
        return EventOut(**result_dict)
    except Exception as e:
        print(f"Terjadi kesalahan internal saat memproses /events/{event_id}: {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal pada server.")