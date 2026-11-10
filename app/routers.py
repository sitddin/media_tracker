from fastapi import APIRouter, HTTPException
from app.schemas import MovieCreate, MovieUpdate
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Movie
from sqlalchemy import select

router = APIRouter(prefix="/movies", tags=["Movies"])

movies = [
    {"id": 1, "title": "Inception", "year": 2010},
    {"id": 2, "title": "Interstellar", "year": 2014}
]

@router.get("")
def get_movies(db: Session = Depends(get_db)):
    statement = select(Movie)
    movies = db.scalars(statement).all()
    return movies

@router.get("/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404, 
            detail="Movie not found"
        )

    return movie

@router.post("", status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    new_movie = Movie(
        title = movie.title,
        year = movie.year
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie

@router.delete("/{movie_id}")
def delete_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            movies.remove(movie)
            return {"message": "Movie deleted"}

    raise HTTPException(status_code=404, detail="Movie not found")

@router.put("/{movie_id}")
def update_movie(movie_id: int, updated_movie: MovieCreate):
    for movie in movies:
        if movie["id"] == movie_id:
            movie["title"] = updated_movie.title
            movie["year"] = updated_movie.year
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@router.patch("/{movie_id}")
def patch_movie(movie_id: int, updated_movie: MovieUpdate):
    for movie in movies:
        if movie["id"] == movie_id:
            changes = updated_movie.model_dump(exclude_unset=True)
            movie.update(changes)
            return movie

    raise HTTPException(status_code=404, detail="Movie not found")