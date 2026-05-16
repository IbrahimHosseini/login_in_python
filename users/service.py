# users/service.py
from . import repository
from .schemas import UserRequest, UserUpdateRequest
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

async def register_user(session: AsyncSession, user: UserRequest) -> User:
	new_user = await repository.create_user(session, user)
	await session.commit()
	return new_user

async def update_user(session: AsyncSession, id: int, new_user: UserUpdateRequest) -> User | None:
	updated_user = await repository.update_user(session=session, id=id, new_data=new_user)
	await session.commit()
	return updated_user

async def delete_user(session: AsyncSession, id: int) -> bool:
	deleted_user = await repository.delete_user(session=session, id=id)
	await session.commit()
	return deleted_user