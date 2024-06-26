from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {
        "id": 1,
        "title": "El señor de los anillos",
        "author": "JRR Tolkien",
        "category": "novel",
    },
    {"id": 2, "title": "El hobbit", "author": "JRR Tolkien", "category": "novel"},
    {"id": 3, "title": "Title 3", "author": "Author 3", "category": "novel"},
    {"id": 4, "title": "Title 4", "author": "Author 4", "category": "math"},
    {"id": 5, "title": "Title 5", "author": "Author 5", "category": "math"},
    {"id": 6, "title": "Title 6", "author": "Author 6", "category": "history"},
]


class CreateBook(BaseModel):
    title: str
    author: str
    category: str


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None


class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str


@app.post("/books")
async def create_book(book: CreateBook) -> Book:
    new_book = book.model_dump()
    new_book["id"] = len(BOOKS) + 1

    BOOKS.append(new_book)
    return Book(**new_book)


@app.get("/books")
async def read_all_books(
    category: str | None = None, author: str | None = None
) -> list[Book]:
    filter_books = BOOKS.copy()

    filter_books = [
        book
        for book in filter_books
        if not category or category.casefold() in book["category"].casefold()
    ]

    filter_books = [
        book
        for book in filter_books
        if not author or author.casefold() in book["author"].casefold()
    ]

    return filter_books


@app.get("/books/{id}")
async def read_book_by_id(id: int) -> Book:
    for b in BOOKS:
        if b.get("id") == id:
            return b
    else:
        raise HTTPException(status_code=404, detail=f"{id} Not Found")


@app.put("/books/{id}")
async def update_book_by_id(id: int, book: UpdateBook) -> Book:

    for b in BOOKS:
        if id == b.get("id"):
            if book.title is not None:
                b["title"] = book.title
            if book.author is not None:
                b["author"] = book.author
            if book.category is not None:
                b["category"] = book.category

            return b

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{id}")
async def delete_book_by_id(id: int) -> None:
    for book in BOOKS:
        if book["id"] == id:
            BOOKS.remove(book)
            return None
