from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool = True

    class config:
        orm_mode = True

class BookBase(BaseModel):
    title: str =Field(..., min_length=2, max_length=200)
    author: str =Field(..., min_length=2, max_length=100)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    is_available: bool = True

    class config:
        orm_mode = True

class BorrowRecordBase(BaseModel):
    user_id: int
    book_id: int

class BorrowRecordBase(BorrowRecordBase):
    pass

class BorrowRecord(BorrowRecordBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class config:
        orm_mode = True