# Blogging API

A production-ready REST API built with FastAPI — featuring JWT authentication, PostgreSQL database, file uploads, and automated tests. Deployed live on Render.

**Live API:** [blogging-api-a0u0.onrender.com/docs](https://blogging-api-a0u0.onrender.com/docs)

---

## Features

- **CRUD** — create, read, update, delete blog posts
- **Authentication** — JWT tokens with bcrypt password hashing
- **Database** — SQLAlchemy ORM with SQLite (dev) and PostgreSQL (production)
- **File Uploads** — profile picture upload with static file serving
- **Background Tasks** — async task execution after response is sent
- **Middleware** — request logging and CORS support
- **Testing** — pytest test suite with a separate test database
- **Deployment** — Dockerized and deployed on Render

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database ORM | SQLAlchemy |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) + passlib (bcrypt) |
| Testing | pytest + httpx |
| Server | Uvicorn |
| Deployment | Render |

---

## Project Structure

```
blogging-api/
├── app/
│   ├── main.py           # app setup, middleware, routers
│   ├── database.py       # engine, session, Base
│   ├── models.py         # SQLAlchemy models (Post, User)
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # JWT token creation and verification
│   ├── hashing.py        # bcrypt password hashing
│   ├── dependencies.py   # reusable DI functions
│   └── routers/
│       ├── posts.py      # post routes
│       └── users.py      # auth + user routes
├── tests/
│   └── test_posts.py     # automated tests
├── uploads/              # saved profile pictures
├── Dockerfile
├── requirements.txt
└── .env                  # not committed
```

---

## API Endpoints

### Posts
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/posts` | No | Get all posts |
| GET | `/posts/{id}` | No | Get post by ID |
| POST | `/posts` | Yes | Create a post |
| PUT | `/posts/{id}` | Yes | Update a post |
| DELETE | `/posts/{id}` | Yes | Delete a post |

### Users
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/register` | No | Register a new user |
| POST | `/login` | No | Login and get JWT token |
| POST | `/users/{id}/upload` | Yes | Upload profile picture |

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/roraks24/blogging-api.git
cd blogging-api
```

**2. Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file**
```
SECRET_KEY=your-secret-key-here
```

**5. Run the server**
```bash
fastapi dev app/main.py
```

API is now running at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

---

## Running Tests

```bash
pytest tests/ -v
```

Tests use a separate `test.db` and never touch the real database.

---

## Running with Docker

```bash
docker build -t blogging-api .
docker run -p 8000:8000 blogging-api
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | JWT signing secret |
| `DATABASE_URL` | Database connection string (defaults to SQLite) |

---

## Author

**Rohit Saini** — built in 7 days as a FastAPI learning project.  
GitHub: [@roraks24](https://github.com/roraks24)
