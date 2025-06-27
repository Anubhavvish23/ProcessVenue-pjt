import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRootEndpoint:
    def test_root(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to Book Review API!"
        assert data["status"] == "running"
        assert "endpoints" in data

class TestBooksEndpoints:
    def test_books_test(self):
        """Test the books test endpoint"""
        response = client.get("/books/test")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Books router is working!"
        assert data["status"] == "success"

    def test_get_books(self):
        """Test getting all books"""
        response = client.get("/books/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_book(self):
        """Test creating a new book"""
        book_data = {
            "title": "Test Book",
            "author": "Test Author"
        }
        response = client.post("/books/", json=book_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert "id" in data

class TestReviewsEndpoints:
    def test_reviews_test(self):
        """Test the reviews test endpoint"""
        response = client.get("/reviews/test")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Reviews router is working!"
        assert data["status"] == "success"

    def test_get_reviews(self):
        """Test getting reviews for a book"""
        response = client.get("/reviews/1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_review(self):
        """Test creating a new review"""
        review_data = {
            "content": "Great book!",
            "rating": 5
        }
        response = client.post("/reviews/?book_id=1", json=review_data)
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == review_data["content"]
        assert data["rating"] == review_data["rating"]
        assert data["book_id"] == 1
        assert "id" in data

class TestDocumentationEndpoints:
    def test_docs(self):
        """Test the docs endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc(self):
        """Test the redoc endpoint"""
        response = client.get("/redoc")
        assert response.status_code == 200

class TestErrorHandling:
    def test_invalid_book_id(self):
        """Test getting reviews for non-existent book"""
        response = client.get("/reviews/999")
        assert response.status_code == 200
        assert response.json() == []

    def test_invalid_json(self):
        """Test creating book with invalid JSON"""
        response = client.post("/books/", data="invalid json")
        assert response.status_code == 422 