from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.pydantic_schemas import UserCreate, UserLogin
from utils.security import create_access_token, get_password_hash, verify_password, decode_access_token

class AuthService:
    """
    Business logic service for user authentication, registration, and token validation.
    """

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieves a user entity by email address.
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        Retrieves a user entity by primary key ID.
        """
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @classmethod
    async def register_user(cls, db: AsyncSession, user_in: UserCreate) -> User:
        """
        Registers a new user account. Ensures email uniqueness and hashes raw password.
        """
        existing_user = await cls.get_user_by_email(db, user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists.",
            )

        hashed_password = get_password_hash(user_in.password)
        new_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            role=user_in.role or "architect",
            is_active=True,
            is_superuser=False,
        )

        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)
        return new_user

    @classmethod
    async def authenticate_user(cls, db: AsyncSession, login_data: UserLogin) -> User:
        """
        Authenticates user credentials and checks account status.
        """
        user = await cls.get_user_by_email(db, login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated.",
            )

        return user

    @classmethod
    async def get_current_user_from_token(cls, db: AsyncSession, token: str) -> User:
        """
        Decodes JWT bearer token and resolves active User entity.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = decode_access_token(token)
        if not payload:
            raise credentials_exception

        email: str = payload.get("email")
        if not email:
            raise credentials_exception

        user = await cls.get_user_by_email(db, email)
        if not user or not user.is_active:
            raise credentials_exception

        return user
