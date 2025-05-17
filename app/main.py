from fastapi import FastAPI
from app.database import database
from app.routers import event, group, weapon, target, region, country, attack


app = FastAPI(title="Global Terrorism API - Group 4")

app.include_router(event.router)
app.include_router(group.router)
app.include_router(weapon.router)
app.include_router(target.router)
app.include_router(region.router)
app.include_router(country.router)
app.include_router(attack.router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()