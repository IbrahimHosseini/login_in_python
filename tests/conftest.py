# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from users.repository import create_user
from users.schemas import UserRequest

from main import app
from db.base import Base
from db.session import get_db

TEST_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5433/test_db"

@pytest.fixture(scope = "session")
async def engine():
	engine = create_async_engine(TEST_DATABASE_URL)
	
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
	yield engine

	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
	await engine.dispose()


@pytest.fixture
async def db_session(engine):
	async with AsyncSession(engine) as session:
		yield session
		await session.rollback()


@pytest.fixture
async def client(db_session):
	async def override_get_db():
		yield db_session

	app.dependency_overrides[get_db] = override_get_db

	async with AsyncClient(
		transport = ASGITransport(app = app),
		base_url = "http://test"
	) as ac:
		yield ac

	app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):
	user = await create_user(
			session = db_session,
			user = UserRequest(
					email = "test@test.com",
					password = "test@1234!"
			)
	)
	return user
