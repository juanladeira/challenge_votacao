from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import logger
from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fator XII: Não criamos tabelas aqui — Alembic gerencia o esquema.
    logger.info(f"Iniciando {settings.PROJECT_NAME} (debug={settings.DEBUG}).")
    yield
    logger.info(f"Encerrando {settings.PROJECT_NAME} (graceful shutdown).")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}
