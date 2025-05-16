from typing import Union # Importing Union for typing hints
from fastapi import FastAPI, Body, HTTPException, status # Importing FastAPI
from fastapi.responses import HTMLResponse # Importing HTMLResponse

app = FastAPI() # Create an instance

movies = [
    {
        "id": 1,
        "title": "Mufasa",
        "overview": "A lion cub's journey to become king",
        "year": 2023,
        "rating": 8.5,
        "category": "Animation"
    },
    
    {
        "id": 2,
        "title": "Harry Potter",
        "overview": "A young wizard's adventures",
        "year": 2001,
        "rating": 9.0,
        "category": "Fantasy"
    }
]

@app.get("/", tags=["Home"])
def user_welcome():
    return HTMLResponse("<h1>Welcome</h1>")

@app.get("/movies", tags=["Movies"])
def list_movies():
    return movies

@app.get("/movies/", tags=["Movies"]) # Query Parameter
def search_movie(title: str):
    for movie in movies:
        if movie["title"] == title:
            return HTMLResponse(f"{movie}")
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Movie not found."
    )

@app.post("/movies", tags=["Movies"])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year:int = Body(), rating:float = Body(), category: str = Body()):
    
    for movie in movies:
        if movie["id"] == id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The movie already exists."
            )
    
    new_movie = {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    }
    
    movies.append(new_movie)
    return HTMLResponse(f"Movie {title} created")

@app.put("/movies/{id}", tags=["Movies"]) # Path Parameter
def update_movie(id: int, title: str = Body(), overview: str = Body(), year:int = Body(), rating:float = Body(), category: str = Body()):
    for movie in movies:
        old_movie_title = movie["title"]
        if movie["id"] == id:
            
            movie["title"] = title
            movie["overview"] = overview
            movie["year"] = year
            movie["rating"] = rating
            movie["category"] = category
            
            return HTMLResponse(f"The movie {old_movie_title} has been updated to {movie['title']}")
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Movie not found."
    )

@app.delete("/movies/{id}") # Path Parameter
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return HTMLResponse(f"The movie {movie['title']} has been deleted")
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Movie not found."
    )