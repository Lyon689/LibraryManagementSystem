from fastapi import APIRouter, HTTPException, Path, status
from typing import List

from models import Book, BookCreate
from storage import storage

book_router = APIRouter(prefix="/books", tags=["books"])

@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    new_book = storage.create_book(book.dict())
    return new_book

@book_router.get("/", response_model=List[Book])
def read_books():
    return list(storage.books.values())

@book_router.get("/{book_id}", response_model=Book)
def read_book(
    book_id: int = Path(..., gt=0, description="The ID of the book to retrieve")
):
    book = storage.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
        )
    return book

@book_router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book: BookCreate
):
    existing_book = storage.get_book(book_id)
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
        )
    
    updated_book = storage.update_book(book_id, book.dict())
    return updated_book

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if not storage.delete_book(book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
        )
    return None

@book_router.put("/{book_id}/unavailable", response_model=Book)
def mark_book_unavailable(book_id: int):
    book = storage.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
        )
    
    updated_book = storage.update_book(book_id, {"is_available": False})
    return updated_book