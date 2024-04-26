from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: int


class CreateBook(BaseModel):
    title: str
    author: str
    category: str
    description: str
    rating: int


class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[int] = None


BOOKS = [
    Book(
        id=1,
        title="El señor de los anillos",
        author="JRR Tolkien",
        category="novel",
        description="EL mejor libro de todos los tiempos",
        rating=5,
    ),
    Book(
        id=2,
        title="El hobbit",
        author="JRR Tolkien",
        category="novel",
        description="El segundo mejor libro de todos los tiempos",
        rating=5,
    ),
    Book(
        id=3,
        title="Harry Potter",
        author="JK Rowling",
        category="novel",
        description="Harry potter es gay",
        rating=1,
    ),
    Book(
        id=4,
        title="Harry Potter 2",
        author="JK Rowling",
        category="novel",
        description="Hermioni esta buenisíma!",
        rating=4,
    ),
]


@app.post("/books")
async def create_book(book: CreateBook) -> Book:
    print(book)
    new_book = Book(**book.model_dump(), id=len(BOOKS) + 1)
    BOOKS.append(new_book)

    return new_book


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
        if b.id == id:
            return b
    else:
        raise HTTPException(status_code=404, detail=f"{id} Not Found")


@app.put("/books/{id}")
async def update_book_by_id(id: int, book: UpdateBook) -> Book:

    for b in BOOKS:
        if id == b.id:
            if book.title is not None:
                b.title = book.title
            if book.author is not None:
                b.author = book.author
            if book.category is not None:
                b.category = book.category
            if book.description is not None:
                b.description = book.description
            if book.rating is not None:
                b.rating = book.rating

            return b

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{id}")
async def delete_book_by_id(id: int):
    for book in BOOKS:
        if book.id == id:
            BOOKS.remove(book)
            return None
