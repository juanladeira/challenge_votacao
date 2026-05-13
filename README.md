# Challenge Votação - API de Intenções de Voto

API simples e robusta para coleta e consulta de intenções de voto, desenvolvida como parte de um desafio técnico. O projeto utiliza uma arquitetura modular e escalável, pronta para produção.

---

## 🏗️ Arquitetura do Projeto

O projeto segue uma arquitetura baseada em **Domínios**, onde cada funcionalidade de negócio é isolada. Para cada domínio, aplicamos o padrão de **5 camadas**:

1.  **`model.py`**: Definição das tabelas do banco de dados utilizando SQLAlchemy (ORM).
2.  **`schema.py`**: Contratos de entrada e saída de dados utilizando Pydantic (Validação e Serialização).
3.  **`repository.py`**: Abstração da camada de dados, contendo apenas consultas SQL e operações de persistência.
4.  **`service.py`**: Camada de lógica de negócio (Regras, validações complexas e orquestração).
5.  **`router.py`**: Definição dos endpoints FastAPI e injeção de dependências.

### Tecnologias Utilizadas
- **Python 3.12+**
- **FastAPI**: Framework web moderno e assíncrono.
- **SQLAlchemy 2.0 + PostgreSQL**: Persistência de dados com suporte total a `asyncio`.
- **Alembic**: Gerenciamento de migrações de banco de dados.
- **Docker & Docker Compose**: Containerização completa do ambiente (API, DB, Redis).
- **uv**: Gerenciador de pacotes extremamente rápido.
- **Pytest**: Framework de testes automatizados.

---

## 📈 Plano de Implementação

O desenvolvimento foi dividido em fases estratégicas, cada uma isolada em sua própria branch para manter o histórico de versionamento limpo e revisável:

### **Fase 1: Conserto da Infraestrutura (Finalizada)**
- Limpeza do template original e remoção de domínios não utilizados.
- Padronização do nome do projeto para `challenge_votacao`.
- Configuração do ambiente Docker e ajuste de portas.
- Implementação de Health-check e estabilização do núcleo da API.
- Documentação inicial e limpeza de arquivos residuais (`.env.example`, scripts).

### **Fase 2: Implementação e Validação (Finalizada)**
- Implementação completa do domínio `votacao` (Model, Schema, Repository, Service e Router).
- Gerenciamento de persistência com migrações Alembic (tabela `votos`).
- Implementação de uma suíte de testes robusta cobrindo 100% das regras de negócio.
- Criação de atalhos via `Makefile` para produtividade.

---

## 🧪 Cenários de Teste

A aplicação conta com testes automatizados que validam os seguintes cenários:

1.  **Listagem de Candidatos**: Garante que o endpoint `GET /candidatos` retorna a lista fixa corretamente. [[Ver teste]](backend/tests/domains/test_votacao.py)
2.  **Voto com Sucesso**: Valida o registro de um voto válido no banco de dados. [[Ver teste]](backend/tests/domains/test_votacao.py)
3.  **Bloqueio de Duplicidade (CPF)**: Garante que um mesmo CPF não pode votar mais de uma vez (Retorna `409 Conflict`). [[Ver teste]](backend/tests/domains/test_votacao.py)
4.  **Candidato Inexistente**: Valida que votos para IDs de candidatos fora da lista fixa sejam rejeitados (Retorna `400 Bad Request`). [[Ver teste]](backend/tests/domains/test_votacao.py)
5.  **Formato de CPF**: Valida se o CPF contém exatamente 11 dígitos numéricos via Pydantic (Retorna `422 Unprocessable Entity` para formatos inválidos). [[Ver teste]](backend/tests/domains/test_votacao.py)
6.  **Agregação de Resultados**: Valida se o cálculo do total de votos e dos percentuais por candidato está correto e arredondado para duas casas decimais. [[Ver teste]](backend/tests/domains/test_votacao.py)

> Todos os testes de domínio podem ser encontrados em: [`backend/tests/domains/`](backend/tests/domains/)

---

## 🛠️ Atalhos Úteis (Makefile)

Para facilitar o desenvolvimento e a avaliação, o projeto inclui um `Makefile` com os comandos mais comuns:

- `make up`: Sobe o ambiente completo em background.
- `make logs`: Acompanha os logs da API.
- `make test`: Executa a suíte de testes (pytest).
- `make migrate-up`: Aplica as migrações no banco de dados.
- `make shell`: Acessa o terminal dentro do container da API.
- `make help`: Lista todos os comandos disponíveis.

---

## 🚀 Como Rodar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/JuanLadeira/challenge_votacao.git
    cd challenge_votacao
    ```

2.  **Configure o ambiente:**
    ```bash
    cp .env.example .env
    ```

3.  **Suba os containers:**
    ```bash
    make up
    ```

4.  **Acesse a API:**
    - Health Check: `http://localhost:8010/health`
    - Documentação Interativa (Swagger): `http://localhost:8010/docs`

5.  **Rodar os Testes:**
    ```bash
    make test
    ```

---

## ⚖️ Estratégia de Escalabilidade (Milhões de Votos)

Para escalar esta aplicação para milhões de votos, as seguintes evoluções arquiteturais seriam implementadas:

### 1. Desacoplamento com Padrão Outbox + Celery
Atualmente, o voto é gravado de forma síncrona. Em um cenário de alta carga:
- O endpoint `/votos` apenas gravaria a intenção de voto e um evento na tabela de **Outbox** dentro da mesma transação.
- Um worker **Celery** processaria essa fila em background para realizar tarefas pesadas (ex: analytics, notificações, auditoria).
- Isso garante que a resposta ao usuário seja na ordem de milissegundos, independentemente do processamento posterior.

### 2. Cache de Resultados com Redis
O endpoint `/resultados` faz agregações no banco. Para milhões de votos:
- Utilizaríamos o **Redis** para armazenar o resultado pré-calculado.
- O cache seria invalidado ou atualizado de forma assíncrona (ex: a cada 10 segundos ou via stream de eventos), evitando sobrecarga no banco de dados relacional.

### 3. Database Sharding e Réplicas de Leitura
- **Réplicas de Leitura:** O tráfego de consulta de resultados seria direcionado para réplicas, deixando o banco primário apenas para inserções de votos.
- **Sharding por CPF:** Divisão dos dados em múltiplos bancos de dados com base no hash do CPF, permitindo escala horizontal da camada de dados.

### 4. Rate Limiting e Proteção
- Implementação de limites de requisição por IP e por CPF na camada de infraestrutura (Nginx/Kong) para evitar ataques de negação de serviço (DDoS) e bots.
