from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from .errors import(
    create_exception_handler,
    InsufficientPermission,
    InvalidToken,
    BookNotFound,
    UserAlreadyExists,
    UserNotFound,
    AccessTokenRequired,
    RefreshTokenRequired,
    InvalidCredentials,
    RevokedToken
    
)

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting ...")
    await init_db() #It is a call routine function so it has to always be called with await.
    yield
    print(f"server has been stopped")

version = "v1"

app = FastAPI(
    title="Bookly",
    version=version,
    description="A REST API for a book review web service",
    # lifespan=life_span
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User with email already exists",
            "error_code": "user_exists"
            
        }
    )
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Book not found",
            "error_code": "book_not_found"
            
        }
    )
)

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Invalid Email or Password",
            "error_code": "invalid_email_or_password"
            
        }
    )
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Token is invalid or expired",
            "resolution": "Please get new token",
            "error_code": "invalid_token"
            
        }
    )
)

app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Token is invalid or has been revoked",
            "resolution": "Please get a new token",
            "error_code": "token_revoked"
            
        }
    )
)

app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Please provide a valid access token",
            "resolution": "Please get an access token",
            "error_code": "user_exists"
            
        }
    )
)

app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Please get a refresh token",
            "resolution": "Please get a refresh token",
            "error_code": "refresh_token_required"
            
        }
    )
)

app.add_exception_handler(
    InsufficientPermission,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "You are not permitted to access this endpoint",
            "error_code": "user_exists"
            
        }
    )
)

@app.exception_handler(500)
async def internal_server_error(request, exc):
    return JSONResponse(
        content={
            "message": "Oops! Something went wrong",
            "error_code": "server_error"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])