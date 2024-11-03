from fastapi import FastAPI
from app.database import engine
from app.routers import prompts, responses
from app.utils.logger import get_logger
from app.utils.error_handler import handle_exception
from app.utils.auth import authenticate_user  # (If JWT authentication is implemented)
from fastapi.middleware.cors import CORSMiddleware  # (If CORS is needed)
from app.config import settings

app = FastAPI()

# Configure CORS (if needed)
origins = ["*"]  # (Replace with your actual allowed origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection (using SQLAlchemy)
@app.on_event("startup")
async def startup():
    await database.connect(settings.DATABASE_URL)
    logger = get_logger(settings.LOG_LEVEL)  # Initialize the logger
    logger.info("Application Startup - Database Connected")


# Close database connection
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("Application Shutdown - Database Disconnected")


# Include API routers
app.include_router(prompts.router)
app.include_router(responses.router)


# Implement JWT authentication middleware (if needed)
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if settings.DEBUG:
        response = await call_next(request)
        return response
    else:
        try:
            await authenticate_user(request)  # Authenticate user
            response = await call_next(request)
            return response
        except Exception as e:
            logger = get_logger(settings.LOG_LEVEL)
            logger.error(f"Authentication Error: {e}")
            raise HTTPException(status_code=401, detail="Unauthorized")


# Define exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger = get_logger(settings.LOG_LEVEL)
    return handle_exception(exc, logger, request)


# Start the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)