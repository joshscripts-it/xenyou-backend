from fastapi import FastAPI
from app.routers import search
from app.routers import search, hostels, interactions, recommend
from app.services.scheduler import periodic_training
import asyncio


app = FastAPI(title="XenYou API")

# Routers
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(hostels.router, prefix="/api/hostels", tags=["Hostels"])
app.include_router(
    interactions.router, prefix="/api/interactions", tags=["Interactions"]
)
app.include_router(recommend.router, prefix="/api/recommend", tags=["Recommender"])


# Services
@app.on_event("startup")
async def startup_event():
    # Run recommender auto-training in background (every 24h = 86400s)
    asyncio.create_task(periodic_training(app, interval=86400))


# Api Root
@app.get("/")
def root():
    return {"message": "Welcome to XenYou 🚀"}
