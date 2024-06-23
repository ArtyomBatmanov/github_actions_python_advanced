from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 10


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/recipes/", response_model=list[schemas.Recipe])
def read_recipes(
    skip: int = DEFAULT_SKIP,
    limit: int = DEFAULT_LIMIT,
    db: Session = Depends(get_db)
):
    recipes = crud.get_recipes(db, skip=skip, limit=limit)
    return recipes


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = crud.get_recipe(db, recipe_id=recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db)
):
    return crud.create_recipe(db=db, recipe=recipe)
