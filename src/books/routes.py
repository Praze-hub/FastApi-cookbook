from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.books.schemas import Book, BookDetailModel, BookUpdateModel, BookCreateModel
from src.books.service import BookService
from typing import List
from src.db.main import get_session
from src.errors import BookNotFound


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin',"user"]))



@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict =Depends(access_token_bearer),
):
    # print(user_details)
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/user/{user_uid}", response_model=List[Book], dependencies=[role_checker])
async def get_user_book_submissions(
    user_uid:str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    # print(user_details)
    books = await book_service.get_user_books(user_uid, session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(
        get_session,
    ),
    token_details: dict=Depends(access_token_bearer),

) -> dict:
    user_id = token_details.get('user')['user_uid']
    # new_book = book_data.model_dump()
    # books.book_router(new_book)
    new_book = await book_service.create_book(book_data,user_id, session)

    return new_book


@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict=Depends(access_token_bearer),
) -> dict:
    # for book in books:
    #     if book["id"] == book_id:
    book = await book_service.get_book(book_uid, session)
    # return book
    if book:
        return book
    else:
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        # )
        raise BookNotFound()


@book_router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict=Depends(access_token_bearer),
) -> dict:
    # for book in books:
    #     if book["id"] == book_id:
    #         book['title'] = book_update_data.title
    #         book['author'] = book_update_data.author
    #         book['publisher'] = book_update_data.publisher
    #         book['page_count'] = book_update_data.page_count

    #         return book
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        # )
        raise BookNotFound()
    else:
        return updated_book


@book_router.delete("/{book_uid}", status_code=status.HTTP_404_NOT_FOUND, dependencies=[role_checker])
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict=Depends(access_token_bearer),
) -> dict:
    # for book in books:
    #     if book["id"] == book_id:
    #         books.remove(book)
    #         #specify return of empty dict
    #         return {}

    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        # )
        raise BookNotFound()
    else:
        return {}
