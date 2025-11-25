from fastapi import FastAPI
from main_router import router as storage_router
from external_router import router as external_router

app = FastAPI()

app.include_router(storage_router)
app.include_router(external_router)