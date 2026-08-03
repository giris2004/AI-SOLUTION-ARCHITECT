from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from models.user import User
from models.pydantic_schemas import Token, UserCreate, UserLogin, UserResponse
from services.auth_service import AuthService
from utils.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    FastAPI dependency for resolving current authenticated user from JWT Bearer header.
    """
    return await AuthService.get_current_user_from_token(db, token)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new solution architect account",
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Creates a new solution architect account in the system.
    """
    user = await AuthService.register_user(db, user_in)
    return user

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and receive JWT access token",
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Authenticates user credentials and generates a signed JWT token.
    """
    user = await AuthService.authenticate_user(db, login_data)
    token_claims = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
    }
    access_token = create_access_token(token_claims)
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve current authenticated user profile",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Returns the authenticated user details for active sessions.
    """
    return current_user
