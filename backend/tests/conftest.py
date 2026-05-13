import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.database import Base
from app.core.settings import settings
from app.main import app

TEST_DATABASE_URL = settings.DATABASE_URL


@pytest.fixture(scope="function", autouse=True)
async def setup_test_db():
    """Garante que todas as tabelas existem no banco de testes."""
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def client():
    """Cria um cliente HTTP para os testes."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
