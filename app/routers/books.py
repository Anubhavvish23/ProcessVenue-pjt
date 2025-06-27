from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import schemas, crud
from app.database import get_db
from app.cache import get_cache, set_cache
import traceback

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=list[schemas.Book])
async def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get all books with pagination"""
    print(f"📚 GET /books/ called with skip={skip}, limit={limit}")
    try:
        # Try to get from cache first
        try:
            cache_key = f"books_{skip}_{limit}"
            cached_books = await get_cache(cache_key)
            if cached_books:
                print("✅ Returning cached books")
                return cached_books
        except Exception as cache_error:
            print(f"⚠️ Cache error (continuing without cache): {cache_error}")
        
        # Fetch from database
        print("🔄 Fetching books from database")
        books = crud.get_books(db, skip=skip, limit=limit)
        print(f"✅ Retrieved {len(books)} books from database")
        
        # Try to cache the result
        try:
            await set_cache(cache_key, [book.__dict__ for book in books])
            print("✅ Books cached successfully")
        except Exception as cache_error:
            print(f"⚠️ Failed to cache books: {cache_error}")
        
        return books
        
    except SQLAlchemyError as db_error:
        print(f"❌ Database error: {db_error}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection error: {str(db_error)}"
        )
    except Exception as e:
        print(f"❌ Unexpected error in read_books: {e}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book"""
    print(f"📚 POST /books/ called with book: {book.title}")
    try:
        db_book = crud.create_book(db, book)
        # Clear cache for books list
        try:
            await set_cache("books_0_10", None, ex=1)  # Invalidate cache
            print("✅ Cache invalidated")
        except Exception as cache_error:
            print(f"⚠️ Failed to invalidate cache: {cache_error}")
        
        print(f"✅ Created book: {db_book.title}")
        return db_book
    except SQLAlchemyError as db_error:
        print(f"❌ Database error in create_book: {db_error}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database error: {str(db_error)}"
        )
    except Exception as e:
        print(f"❌ Error in create_book: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/test")
async def test_books():
    """Simple test endpoint to verify router is working"""
    return {"message": "Books router is working!", "status": "success"}
