from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import schemas, crud
from app.database import get_db
from app.cache import get_cache, set_cache
import traceback

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@router.get("/test")
async def test_reviews():
    """Simple test endpoint to verify router is working"""
    return {"message": "Reviews router is working!", "status": "success"}

@router.get("/{book_id}", response_model=list[schemas.Review])
async def read_reviews(book_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a specific book"""
    print(f"📝 GET /reviews/{book_id} called")
    try:
        # Try to get from cache first
        try:
            cache_key = f"reviews_{book_id}"
            cached_reviews = await get_cache(cache_key)
            if cached_reviews:
                print("✅ Returning cached reviews")
                return cached_reviews
        except Exception as cache_error:
            print(f"⚠️ Cache error (continuing without cache): {cache_error}")
        
        # Fetch from database
        print("🔄 Fetching reviews from database")
        reviews = crud.get_reviews_by_book(db, book_id)
        print(f"✅ Retrieved {len(reviews)} reviews from database")
        
        # Try to cache the result
        try:
            await set_cache(cache_key, [review.__dict__ for review in reviews])
            print("✅ Reviews cached successfully")
        except Exception as cache_error:
            print(f"⚠️ Failed to cache reviews: {cache_error}")
        
        return reviews
        
    except SQLAlchemyError as db_error:
        print(f"❌ Database error: {db_error}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection error: {str(db_error)}"
        )
    except Exception as e:
        print(f"❌ Unexpected error in read_reviews: {e}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=schemas.Review)
async def create_review(review: schemas.ReviewCreate, book_id: int, db: Session = Depends(get_db)):
    """Create a new review for a book"""
    print(f"📝 POST /reviews/ called for book_id: {book_id}")
    try:
        db_review = crud.create_review(db, review, book_id)
        # Clear cache for this book's reviews
        try:
            await set_cache(f"reviews_{book_id}", None, ex=1)  # Invalidate cache
            print("✅ Cache invalidated")
        except Exception as cache_error:
            print(f"⚠️ Failed to invalidate cache: {cache_error}")
        
        print(f"✅ Created review for book {book_id}")
        return db_review
    except SQLAlchemyError as db_error:
        print(f"❌ Database error in create_review: {db_error}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(db_error)}"
        )
    except Exception as e:
        print(f"❌ Error in create_review: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
