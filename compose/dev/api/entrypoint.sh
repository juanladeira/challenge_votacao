#!/bin/bash
set -e

echo "[entrypoint] Rodando migrações Alembic..."
# uv run alembic upgrade head || echo "[entrypoint] Aviso: Falha ao rodar migrações (provavelmente banco vazio ou sem revisões ainda)."

echo "[entrypoint] Pronto. Iniciando servidor..."
exec "$@"
