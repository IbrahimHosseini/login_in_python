# db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import settings

engin = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

AsyncSessionFactory = async_sessionmaker(
    engin,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionFactory() as session:
        yield session