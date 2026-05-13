import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_listar_candidatos(client: AsyncClient):
    """Testa se a lista de candidatos é retornada corretamente."""
    response = await client.get("/candidatos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == "Maria Silva"
    assert data[1]["nome"] == "João Souza"


@pytest.mark.asyncio
async def test_registrar_voto_sucesso(client: AsyncClient):
    """Testa o registro de um voto com sucesso."""
    voto_data = {"cpf": "12345678901", "candidato_id": 1}
    response = await client.post("/votos", json=voto_data)
    assert response.status_code == 201
    assert response.json() == {"message": "Voto registrado com sucesso"}


@pytest.mark.asyncio
async def test_registrar_voto_cpf_duplicado(client: AsyncClient):
    """Testa se o mesmo CPF não pode votar duas vezes."""
    voto_data = {"cpf": "11122233344", "candidato_id": 1}

    # Primeiro voto
    await client.post("/votos", json=voto_data)

    # Segundo voto (mesmo CPF)
    response = await client.post("/votos", json=voto_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "Este CPF já registrou um voto"


@pytest.mark.asyncio
async def test_registrar_voto_candidato_inexistente(client: AsyncClient):
    """Testa se não é possível votar em um candidato que não existe."""
    voto_data = {"cpf": "99988877766", "candidato_id": 99}
    response = await client.post("/votos", json=voto_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Candidato inexistente"


@pytest.mark.asyncio
async def test_registrar_voto_cpf_invalido(client: AsyncClient):
    """Testa a validação de formato do CPF (11 dígitos)."""
    votos_invalidos = [
        {"cpf": "123", "candidato_id": 1},  # Curto
        {"cpf": "123456789012", "candidato_id": 1},  # Longo
        {"cpf": "abc45678901", "candidato_id": 1},  # Letras
    ]
    for voto in votos_invalidos:
        response = await client.post("/votos", json=voto)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_obter_resultados(client: AsyncClient):
    """Testa o cálculo e retorno dos resultados."""
    # Simula alguns votos
    await client.post("/votos", json={"cpf": "00000000001", "candidato_id": 1})
    await client.post("/votos", json={"cpf": "00000000002", "candidato_id": 1})
    await client.post("/votos", json={"cpf": "00000000003", "candidato_id": 2})

    response = await client.get("/resultados")
    assert response.status_code == 200
    data = response.json()

    assert data["total_votos"] == 3
    # Candidato 1: 2 votos (66.67%)
    # Candidato 2: 1 voto (33.33%)

    results = {c["id"]: c for c in data["candidatos"]}
    assert results[1]["votos"] == 2
    assert results[1]["percentual"] == 66.67
    assert results[2]["votos"] == 1
    assert results[2]["percentual"] == 33.33
