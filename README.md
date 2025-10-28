# Mini Blog API

A FastAPI-based mini blog project supporting **users, posts, comments, and likes**. This project demonstrates SQLAlchemy ORM, PostgreSQL integration, JWT authentication, and password hashing with Passlib (bcrypt).

---

## Features
- User registration and authentication (JWT)
- Create, read, update, delete posts
- Comment on posts
- Like posts
- Pagination for posts and comments
- Relational database handling using SQLAlchemy

---

## Tech Stack / Dependencies
- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- psycopg2-binary
- Passlib (bcrypt)

You can install all dependencies with:

## Clone the repository:
```bash
git clone https://github.com/<username>/mini-blog-fastapi.git
cd mini-blog-fastapi
```

## Create a virtual environment (optional but recommended):
```bash
pipenv --python 3.13
pipenv install fastapi uvicorn
```

## activate virtual environment
```bash
pipenv shell
```
## Install dependencies:
```bash
pip install -r requirements.txt
```

## A blog database must be created in postgresql

## Initialize Alembic (first time only)
```
alembic init alembic
```
### In alembic.ini
```
sqlalchemy.url = driver://user:pass@localhost/blog
```

### In alembic/env.py
```
from serveces.database import Base
from models.user impotr User
from models.post import Post
from models.comment import Comment
from models.like import Like
target_metadata = Base.metadata
```

### Create a new migration
```
alembic revision --autogenerate -m "create initial tables"
```

### Apply migration to database
```
alembic upgrade head
```

## Run the application:
```bash
uvicorn app.main:app --reload
py main.py
```
## The API will be available at: 
```bash

http://127.0.0.1:8000
```
