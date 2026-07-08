from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import interactions, chat
from app.db.database import Base, engine
from app.core.config import settings
from app.core.logger import logger

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-First CRM HCP Module")

# Configure CORS
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response Status: {response.status_code}")
    return response

app.include_router(interactions.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-First CRM API"}
