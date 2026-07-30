from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models.contact import Contact

from app.routes import services, contact

app = FastAPI()

Base.metadata.create_all(bind=engine)

# CORS middleware remains here
# app.add_middleware(...)

# Routers remain here
# app.include_router(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router, prefix="/api", tags=["Services"])

app.include_router(contact.router,  prefix="/api" , tags=["Contact"])

@app.get("/")
def home():

    return {

        "message": "Welcome to the Novixa API!"

    }