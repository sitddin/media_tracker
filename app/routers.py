from fastapi import APIRouter, HTTPException
from app.schemas import MovieCreate, MovieUpdate
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Movie
from sqlalchemy import select
import httpx
from app.tmdb import search_movies, get_movie_details
from app.dependencies import get_current_user
from app.models import User


router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/search")
def search_movies_endpoint(title: str):
    try:
        data = search_movies(title)

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="TMDB request timed out"
        )
    
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="TMDB returned an error"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to TMDB"
        )

    movies = []

    for movie in data["results"]:
        movies.append({
            "tmdb_id": movie["id"],
            "title": movie["title"],
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average")
        })

    return movies

@router.get("")
def get_movies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(Movie).where(
        Movie.user_id == current_user.id
    )

    movies = db.scalars(statement).all()
    return movies

@router.post("/import/{tmdb_id}", status_code=201)
def import_movie(tmdb_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing_movie = db.scalar(
    select(Movie).where(
        Movie.tmdb_id == tmdb_id,
        Movie.user_id == current_user.id
    )
)

    if existing_movie is not None:
        raise HTTPException(
            status_code=409,
            detail="Movie already exists in collection"
        )
    
    try:
        data = get_movie_details(tmdb_id)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Movie not found in TMDB"
            )

        raise HTTPException(
            status_code=502,
            detail="TMDB returned an error"
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="TMDB request timed out"
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to TMDB"
        )

    release_date = data.get("release_date")

    if not release_date:
        raise HTTPException(
            status_code=422,
            detail="Movie has no release date"
        )

    movie = Movie(
        tmdb_id=tmdb_id,
        title=data["title"],
        year=int(release_date[:4]),
        rating=data.get("vote_average"),
        user_id=current_user.id
    )

    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie

@router.get("/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    movie = db.scalar(
        select(Movie).where(
            Movie.id == movie_id,
            Movie.user_id == current_user.id
        )
    )

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie

@router.post("", status_code=201)
def create_movie(
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_movie = Movie(
        title=movie_data.title,
        year=movie_data.year,
        user_id=current_user.id
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie

@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movie = db.scalar(
        select(Movie).where(
            Movie.id == movie_id,
            Movie.user_id == current_user.id
        )
    )

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    db.delete(movie)
    db.commit()

    return {"message": "Movie deleted"}


@router.put("/{movie_id}")
def update_movie(movie_id: int, updated_movie: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    movie = db.scalar(
        select(Movie).where(
            Movie.id == movie_id,
            Movie.user_id == current_user.id
        )
    )

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
def patch_movie(movie_id: int, updated_movie: MovieUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    movie = db.scalar(
        select(Movie).where(
            Movie.id == movie_id,
            Movie.user_id == current_user.id
        )
    )

    if movie is None:
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