import pytest
import asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def postgres_container():
    """Sobe um container temporário do Postgres para a sessão de testes."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para a sessão de testes."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def engine(postgres_container):
    """Cria o engine apontando para o Testcontainer."""
    # O testcontainers por padrão usa psycopg2 na URL.
    # Precisamos forçar a troca para asyncpg para o SQLAlchemy assíncrono.
    url = postgres_container.get_connection_url().replace(
        "postgresql+psycopg2://", "postgresql+asyncpg://"
    )

    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(engine):
    """Cria uma sessão isolada para o teste."""
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        yield session


@pytest.fixture
async def client(db_session):
    """Cria um cliente HTTP com override de DB apontando para o Testcontainer."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
