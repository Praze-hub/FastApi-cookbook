from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


class BooklyException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BooklyException):
    """User has provided a revoked token"""

    pass


class AccessTokenRequired(BooklyException):
    """Enter valid access token"""

    pass


class RefreshTokenRequired(BooklyException):
    """Enter a valid refresh token"""

    pass


class UserAlreadyExists(BooklyException):
    """User already exists"""

    pass


class UserNotFound(BooklyException):
    """User not found"""

    pass


class InvalidCredentials(BooklyException):
    """User has provided an invalid or Email or Password"""

    pass


class InsufficientPermission(BooklyException):
    """User does not have enough permission to access this endpoint"""

    pass


class BookNotFound(BooklyException):
    """Book not found"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Invalid Email or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Token is invalid or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get a new token",
                "error_code": "token_revoked",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please get a refresh token",
                "resolution": "Please get a refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You are not permitted to access this endpoint",
                "error_code": "user_exists",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
