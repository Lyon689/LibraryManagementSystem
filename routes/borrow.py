from fastapi import APIRouter, HTTPException, Path, status
from typing import List
from datetime import datetime

from models import BorrowRecord, BorrowRecordBase
from storage import storage

borrow_router = APIRouter(prefix="/borrow", tags=["borrow"])

@borrow_router.post("/", response_model=BorrowRecord, status_code=status.HTTP_201_CREATED)
def borrow_book(borrow_record: BorrowRecordBase):
    # Check if user exists and is active
    user = storage.get_user(borrow_record.user_id)
    if not user or not user['is_active']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User is not active or does not exist"
        )

    # Check if book exists and is available
    book = storage.get_book(borrow_record.book_id)
    if not book or not book['is_available']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Book is not available or does not exist"
        )

    # Check if user has already borrowed this book
    user_records = storage.get_user_borrow_records(borrow_record.user_id)
    for record in user_records:
        if (record['book_id'] == borrow_record.book_id and 
            record['return_date'] is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="User has already borrowed this book"
            )

    # Create borrow record
    new_record = storage.create_borrow_record(borrow_record.dict())

    # Mark book as unavailable
    storage.update_book(borrow_record.book_id, {"is_available": False})

    return new_record

@borrow_router.put("/return/{record_id}", response_model=BorrowRecord)
def return_book(record_id: int):
    # Find the borrow record
    record = storage.borrow_records.get(record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Borrow record not found"
        )

    # Check if book is already returned
    if record['return_date']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Book has already been returned"
        )

    # Update return date
    record['return_date'] = datetime.now()
    
    # Mark book as available again
    storage.update_book(record['book_id'], {"is_available": True})

    return record

@borrow_router.get("/user/{user_id}", response_model=List[BorrowRecord])
def get_user_borrow_records(
    user_id: int = Path(..., gt=0, description="The ID of the user")
):
    # Check if user exists
    user = storage.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    return storage.get_user_borrow_records(user_id)

@borrow_router.get("/", response_model=List[BorrowRecord])
def get_all_borrow_records():
    return storage.get_all_borrow_records()