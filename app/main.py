from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from app.routers import books, reviews
from app.database import engine
from app.cache import test_redis_connection

app = FastAPI(
    title="Book Review API",
    description="A FastAPI backend for managing books and reviews with Redis caching",
    version="1.0.0"
)

app.include_router(books.router)
app.include_router(reviews.router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Book Review API!",
        "version": "1.0.0",
        "endpoints": {
            "books": "/books/",
            "reviews": "/reviews/{book_id}",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        },
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint to test database and Redis connections"""
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "redis": "unknown",
        "errors": []
    }
    
    # Test database connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        health_status["database"] = "connected"
        print("✅ Database connection successful")
    except Exception as e:
        health_status["database"] = "error"
        health_status["errors"].append(f"Database: {str(e)}")
        print(f"❌ Database connection failed: {e}")
    
    # Test Redis connection
    try:
        redis_ok = await test_redis_connection()
        health_status["redis"] = "connected" if redis_ok else "error"
        if not redis_ok:
            health_status["errors"].append("Redis: Connection failed")
    except Exception as e:
        health_status["redis"] = "error"
        health_status["errors"].append(f"Redis: {str(e)}")
    
    # Overall status
    if health_status["database"] == "error":
        health_status["status"] = "unhealthy"
    
    return health_status

# Debug: Print all registered routes
print("🔍 Registered routes:")
for route in app.routes:
    print(f"  {route.methods} {route.path}")

print("✅ FastAPI app initialized successfully!")
