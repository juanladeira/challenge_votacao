.PHONY: help up down restart logs shell lint test cov migrate-gen migrate-up clean

# Variáveis
DOCKER_COMPOSE = docker compose
API_SERVICE = api

help: ## Exibe esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Sobe os containers em background
	$(DOCKER_COMPOSE) up -d

down: ## Para os containers e remove redes/volumes
	$(DOCKER_COMPOSE) down

restart: ## Reinicia o serviço da API
	$(DOCKER_COMPOSE) restart $(API_SERVICE)

logs: ## Exibe os logs da API em tempo real
	$(DOCKER_COMPOSE) logs -f $(API_SERVICE)

shell: ## Abre um shell interativo no container da API
	$(DOCKER_COMPOSE) exec $(API_SERVICE) /bin/bash

lint: ## Executa a verificação de lint e formatação (ruff)
	$(DOCKER_COMPOSE) exec $(API_SERVICE) uv run ruff check app tests alembic --fix
	$(DOCKER_COMPOSE) exec $(API_SERVICE) uv run ruff format app tests alembic

test: ## Executa os testes automatizados
	$(DOCKER_COMPOSE) exec $(API_SERVICE) uv run pytest

cov: ## Executa os testes com relatório de cobertura (coverage)
	$(DOCKER_COMPOSE) exec $(API_SERVICE) uv run pytest --cov=app --cov-report=term-missing

migrate-gen: ## Gera uma nova migração (uso: make migrate-gen m="nome_da_migracao")
	$(DOCKER_COMPOSE) exec $(API_SERVICE) uv run alembic revision --autogenerate -m "$(m)"

migrate-up: ## Aplica as migrações pendentes
	$(DOCKER_COMPOSE) exec $(API_SERVICE) uv run alembic upgrade head

clean: ## Limpa caches do python e logs
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
