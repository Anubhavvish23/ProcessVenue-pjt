
# 📚 Book Review API

A modern, high-performance Book Review API built with **FastAPI**, **PostgreSQL**, and **Redis** for efficient data management and caching.

## 🚀 Features

- 📖 CRUD operations on books and reviews
- ⚡ Redis caching for optimized response times
- 📑 Auto-generated Swagger docs
- 🧪 Testing-ready structure
- ✅ Health check endpoint

---

## 🛠️ Tech Stack

| Tech       | Usage                                |
|------------|---------------------------------------|
| FastAPI    | Backend web framework                 |
| SQLAlchemy | ORM for PostgreSQL                    |
| Alembic    | DB migrations                         |
| Redis      | In-memory cache for fast retrieval    |
| Pydantic   | Request/response validation           |
| Uvicorn    | ASGI server for FastAPI               |

---

## 📦 Installation

### 1️⃣ Clone the repo

```bash
git clone https://github.com/your-username/book-review-api.git
cd book-review-api
2️⃣ Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set up PostgreSQL database
Create a PostgreSQL DB named bookdb, and update the connection in app/database.py if needed.

5️⃣ Run Alembic migrations
bash
Copy
Edit
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
🚦 Running the Project
▶️ Start Redis server
bash
Copy
Edit
redis-server
▶️ Run FastAPI server
bash
Copy
Edit
uvicorn app.main:app --reload
Then visit:

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

🔁 API Endpoints
📚 Books
Method	Endpoint	Description
GET	/books/	Get all books
POST	/books/	Create new book

📝 Reviews
Method	Endpoint	Description
GET	/reviews/{book_id}	Get reviews for a book
POST	/reviews/?book_id=x	Create review for a book