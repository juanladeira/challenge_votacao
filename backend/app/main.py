from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.logging import logger
from app.core.settings import settings
from app.domains.votacao.router import router as votacao_router

# Importa o centralizador de modelos para registro no Base.metadata
import app._models  # noqa: F401


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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Transforma erros complexos do Pydantic em mensagens simples."""
    # Pega apenas a primeira mensagem de erro para simplificar a resposta
    error = exc.errors()[0]
    msg = error.get("msg", "Erro de validação").replace("Value error, ", "")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": msg},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(votacao_router)


@app.get(
    "/health",
    status_code=HTTPStatus.OK,
    tags=["Core"],
    description="Endpoint para verificação de saúde do serviço.",
)
async def health():
    return {"status": "ok"}
