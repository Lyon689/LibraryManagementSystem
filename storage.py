from typing import List, Dict, Optional
from datetime import datetime

class InMemoryStorage:
    def __init__(self):
        self.user: Dict[int, dict] = {}
        self.books: Dict[int, dict] = {}
        self.borrow_records: Dict[int, dict] = {}
        self._user_counter = 1
        self._book_counter = 1
        self._borrow_record_counter = 1

    def create_user(self, user: dict) -> dict:
        user['id'] = self._user_counter
        user['is_active'] = user.get('is_active', True)
        self.user[self._user_counter] = user
        self._user_counter += 1
        return user

    def get_user(self, user_id: int) -> Optional[dict]:
        return self.user.get(user_id)

    def update_user(self, user_id: int, user_data: dict) -> Optional[dict]:
        if user_id in self.user:
           self.user[user_id].update(user_data)
           return self.user[user_id]
    
        return None


    def delete_user(self, user_id: int) -> bool:
        if user_id in self.user:
           del self.user[user_id]
           return True
        return False

    def create_book(self, book: dict) -> dict:
        book['id'] = self._book_counter
        book['is_available'] = book.get('is_available', True)
        self.books[self._book_counter] = book
        self._book_counter += 1
        return book

    def get_book(self, book_id: int) -> Optional[dict]:
        return self.books.get(book_id)

    def update_book(self, book_id: int, book_data: dict) -> Optional[dict]:
        if book_id in self.books:
           self.books[book_id].update(book_data)
           return self.books[book_id]
        return None

    def delete_bOOK(self, book_id: int) -> bool:
        if book_id in self.books:
           del self.books[book_id]
           return True
        return False

    def create_borrow_record(self, borrow_record: dict) -> dict:
        borrow_record['id'] = self._borrow_record_counter
        borrow_record['borrow_date'] = datetime.now()
        borrow_record['return_date'] = None
        self.borrow_records [self._borrow_record_counter] = borrow_record
        self._borrow_record_counter += 1
        return borrow_record

    def get_user_borrow_records(self, user_id: int) -> List[dict]:
        return [
            record for record in self.borrow_records.values()
            if record['user_id'] == user_id
        ]

    def get_all_borrow_records(self) -> List[dict]:
        return list(self.borrow_records.values())
    

storage = InMemoryStorage()

