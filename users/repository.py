# users/repository.py

from auth.service import hash_password
from db.models import RefreshToken, User
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserRequest, UserUpdateRequest


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    
    result = await session.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    return user

async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    result = await session.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    return user

async def create_user(session: AsyncSession, user: UserRequest) -> User:
    
    new_user = User(
        email = user.email,
        hashed_password = hash_password(user.password),
    )

    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)

    return new_user

async def update_user(session: AsyncSession, id: int, new_data: UserUpdateRequest) -> User | None:
    result = await session.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        return None

    data = new_data.model_dump(exclude_unset = True)

    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.hashed_password = hash_password(data["password"])

    await session.flush()
    await session.refresh(user)

    return user


async def delete_user(session: AsyncSession, id: int) -> bool:

    await session.execute(
        delete(RefreshToken).where(RefreshToken.user_id == id)
    )

    result = await session.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        return False
        
    await session.delete(user)
    await session.flush()

    return True