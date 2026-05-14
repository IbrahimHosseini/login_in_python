# repository.py

from auth.service import hash_password
from db import session
from db.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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

async def create_user(session: AsyncSession, user: User) -> User:
    
    new_user = User(
        email = user.email,
        hashed_password = hash_password(user.hashed_password),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

async def update_user(session: AsyncSession, id: int, new_data: User) -> User | None:
    result = await session.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        return None

    user.email = new_data.email
    user.hashed_password = hash_password(new_data.hashed_password)

    await session.commit()
    await session.refresh(user)

    return user


async def delete_user(session: AsyncSession, id: int):
    result = await session.execute(
        select(User).where(User.id == id)
    )

    user = result.scalar_one_or_none()

    if user is None:
        return None
        
    await session.delete(user)
    await session.commit()