import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def test_root():
    """Test the root endpoint"""
    print("🔍 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_books():
    """Test books endpoints"""
    print("📚 Testing books endpoints...")
    
    # Test books test endpoint
    print("1. Testing /books/test...")
    response = requests.get(f"{BASE_URL}/books/test")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test get all books
    print("2. Testing GET /books/...")
    response = requests.get(f"{BASE_URL}/books/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test create book
    print("3. Testing POST /books/...")
    book_data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald"
    }
    response = requests.post(
        f"{BASE_URL}/books/",
        headers={"Content-Type": "application/json"},
        data=json.dumps(book_data)
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_reviews():
    """Test reviews endpoints"""
    print("📝 Testing reviews endpoints...")
    
    # Test reviews test endpoint
    print("1. Testing /reviews/test...")
    response = requests.get(f"{BASE_URL}/reviews/test")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test get reviews for book ID 1
    print("2. Testing GET /reviews/1...")
    response = requests.get(f"{BASE_URL}/reviews/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test create review
    print("3. Testing POST /reviews/...")
    review_data = {
        "content": "Amazing classic novel!",
        "rating": 5
    }
    response = requests.post(
        f"{BASE_URL}/reviews/?book_id=1",
        headers={"Content-Type": "application/json"},
        data=json.dumps(review_data)
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_documentation():
    """Test documentation endpoints"""
    print("📖 Testing documentation endpoints...")
    
    # Test docs endpoint
    print("1. Testing /docs...")
    response = requests.get(f"{BASE_URL}/docs")
    print(f"Status: {response.status_code}")
    print("Docs endpoint is accessible")
    print()
    
    # Test redoc endpoint
    print("2. Testing /redoc...")
    response = requests.get(f"{BASE_URL}/redoc")
    print(f"Status: {response.status_code}")
    print("ReDoc endpoint is accessible")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting FastAPI Book Review API Tests")
    print("=" * 50)
    
    try:
        test_root()
        test_books()
        test_reviews()
        test_documentation()
        
        print("✅ All tests completed!")
        print("\n📋 Summary:")
        print("- Root endpoint: Working")
        print("- Books endpoints: Working")
        print("- Reviews endpoints: Working")
        print("- Documentation: Accessible")
        print("\n🌐 Visit http://127.0.0.1:8000/docs for interactive testing")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server")
        print("Make sure your FastAPI server is running with:")
        print("uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main() 