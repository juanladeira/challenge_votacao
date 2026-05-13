import pytest
from app.domains.votacao.router import (
    registrar_voto,
    listar_candidatos,
    obter_resultados,
)
from app.domains.votacao.schema import VotoCreate
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_router_registrar_voto():
    service = AsyncMock()
    voto_data = VotoCreate(cpf="11111111111", candidato_numero=13)
    response = await registrar_voto(voto_data, service)
    assert response == {"message": "Voto registrado com sucesso"}
    service.registrar_voto.assert_called_once_with(voto_data)


@pytest.mark.asyncio
async def test_router_listar_candidatos():
    service = MagicMock()
    await listar_candidatos(service)
    service.listar_candidatos.assert_called_once()


@pytest.mark.asyncio
async def test_router_obter_resultados():
    service = AsyncMock()
    await obter_resultados(service)
    service.obter_resultados.assert_called_once()
