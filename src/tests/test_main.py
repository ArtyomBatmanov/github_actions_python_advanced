from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_recipes.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_recipe():
    response = client.post(
        "/recipes/",
        json={
            "title": "Spaghetti Carbonara",
            "preparation_time": 30,
            "ingredients": "Spaghetti, Eggs, Bacon, Parmesan Cheese",
            "description": "Classic Italian pasta dish with creamy sauce",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Spaghetti Carbonara"
    assert "id" in data
    assert "views" in data


def test_read_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_recipe():
    response = client.post(
        "/recipes/",
        json={
            "title": "Test Recipe",
            "preparation_time": 15,
            "ingredients": "Test Ingredient 1, Test Ingredient 2",
            "description": "This is a test recipe",
        },
    )
    assert response.status_code == 200
    data = response.json()
    recipe_id = data["id"]

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Recipe"


def test_read_recipe_not_found():
    response = client.get("/recipes/999")
    assert response.status_code == 404
