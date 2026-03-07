from fastapi import FastAPI
from app.routers import upload

app = FastAPI()

# Include the separated router
app.include_router(upload.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Portal"}