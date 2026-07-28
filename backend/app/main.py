from fastapi import FastAPI  # type: ignore[import]

from app.routes import services, contact

app = FastAPI(
    title="Novixa API",
    version="1.0.0"
)

app.include_router(
    services.router,
    prefix="/api",
    tags=["Services"]
)
app.include_router(
    contact.router,
    prefix="/api",
    tags=["Contact"]
)

@app.get("/")
def home():

    return {

        "message": "Welcome to the Novixa API!"

    }