from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse

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


def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    
    async def exception_handler(request: Request,exc: BooklyException): 
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
        
    return exception_handler

