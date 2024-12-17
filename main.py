from fastapi import FastAPI
from routes.user import router
from routes.book import book_router
from routes.borrow import borrow_router

app = FastAPI()

app.include_router(router, tags=["Users"], prefix="/v1")
app.include_router(book_router, tags=["Books"])
app.include_router(borrow_router, tags=["Borrows"])



@app.get("/")
def read_root():
    return{"message": "Welcome to the library system management"}