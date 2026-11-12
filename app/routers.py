from fastapi import APIRouter, HTTPException
from app.schemas import MovieCreate, MovieUpdate
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Movie
from sqlalchemy import select

router = APIRouter(prefix="/movies", tags=["Movies"])

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
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404, 
            detail="Movie 
        )
    
    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted"}


@router.put("/{movie_id}")
def update_movie(movie_id: int, updated_movie: MovieCreate, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404, 
            detail="Movie not found"
            )
    movie.title = updated_movie.title
    movie.year = updated_movie.year

    db.commit()
    db.refresh(movie)

    return movie

@router.patch("/{movie_id}")
def patch_movie(movie_id: int, updated_movie: MovieUpdate, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)

    if Movie is None:
        raise HTTPException(
            status_code=404, 
            detail="Movie not found"
            )

    changes = updated_movie.model_dump(exclude_unset=True)

    for field, value in changes.items():
        setattr(movie, field, value)

    db.commit()
    db.refresh(movie)

    return movie