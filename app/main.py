from fastapi import FastAPI
from app.routers.conversation import router

app = FastAPI(
    title="Personalized Networking Assistant",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Personalized Networking Assistant API Running"
    }