from typing import Optional
from fastapi import FastAPI
import uvicorn
from enum import Enum

BOOKS = {
    "book_1": {"title": "Adventures of Sherlok", "author": "Conan Doyle"},
    "book_2": {"title": "Title_2", "author": "Author_2"},
    "book_3": {"title": "Title_3", "author": "Author_3"},

}

class DirectionName(str, Enum):
    south = "South"
    north = "North"
    east = "East"
    west = "West"

app = FastAPI()

@app.get('/')
async def home():
    return {"message": "FAST Api CRUD App"}

@app.get('/books')
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS

@app.get('/books/{book_name}')
async def get_book(book_name: str):
    return BOOKS[book_name]

@app.get('/direction/{direction_name}')
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {"Direction": direction_name, "sub": "Down"}
    if direction_name == DirectionName.west:
        return {"Direction": direction_name, "sub": "left"}
    return {"Direction": direction_name, "sub": "right"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)