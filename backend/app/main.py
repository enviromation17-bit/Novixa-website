from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.v1 import contact
from app.routes.v1 import auth
from app.core.exceptions import global_exception_handler
from app.routes.v1 import  services
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter

app = FastAPI(

    title="Novixa API",

    description="""
Professional AI Engineering Platform

Features:

- Contact API
- Client Lead Management
- Admin Dashboard
- Future AI Assistant
- Future Automation APIs
""",

    version="1.0.0",

    contact={

        "name": "Novixa",

        "email": "hello@novixa.com"

    },

    license_info={

        "name": "MIT"

    }

)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(
    Exception,
    global_exception_handler
)
#Base.metadata.create_all(bind=engine)

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



@app.get("/")
def home():

    return {

        "message": "Welcome to the Novixa API!"

    }
@app.get("/health")
def health():

    return {

        "status": "running",

        "company": "Novixa",

        "version": "1.0.0"

    }
app.include_router(
    auth.router,
    prefix="/api/v1"
)

app.include_router(
    contact.router,
    prefix="/api/v1"
)

app.include_router(
    services.router,
    prefix="/api/v1"
)