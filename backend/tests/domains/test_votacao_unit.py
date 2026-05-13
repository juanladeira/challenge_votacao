import pytest
from app.domains.votacao.service import VotacaoService, CANDIDATOS_FIXOS
from app.domains.votacao.schema import VotoCreate
from fastapi import HTTPException
from unittest.mock import AsyncMock
from hypothesis import given, strategies as st, settings


@pytest.mark.asyncio
async def test_service_registrar_voto_sucesso():
    repo = AsyncMock()
    repo.get_by_cpf.return_value = None
    service = VotacaoService(repo)

    voto = VotoCreate(cpf="99999999999", candidato_numero=13)
    await service.registrar_voto(voto)

    repo.create_by_id.assert_called_once_with(cpf="99999999999", candidato_id=1)


@pytest.mark.asyncio
async def test_service_registrar_voto_candidato_invalido():
    repo = AsyncMock()
    service = VotacaoService(repo)

    voto = VotoCreate(cpf="88888888888", candidato_numero=999)
    with pytest.raises(HTTPException) as exc:
        await service.registrar_voto(voto)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_service_registrar_voto_cpf_duplicado():
    repo = AsyncMock()
    repo.get_by_cpf.return_value = AsyncMock()  # Simula voto existente
    service = VotacaoService(repo)

    voto = VotoCreate(cpf="77777777777", candidato_numero=13)
    with pytest.raises(HTTPException) as exc:
        await service.registrar_voto(voto)
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_service_obter_resultados_vazio():
    repo = AsyncMock()
    repo.get_vote_counts.return_value = {}
    service = VotacaoService(repo)

    resultados = await service.obter_resultados()
    assert resultados.total_votos == 0
    # Verifica se todos os candidatos (2) estão presentes
    assert len(resultados.candidatos) == 2
    assert resultados.candidatos[0].numero == 13


# --- Escalonamento com Hypothesis ---


@settings(max_examples=50, deadline=None)
@given(
    cpf=st.from_regex(r"^\d{11}$", fullmatch=True),
    candidato_num=st.sampled_from([c["numero"] for c in CANDIDATOS_FIXOS]),
)
@pytest.mark.asyncio
async def test_hypothesis_voto_valido(cpf, candidato_num):
    """Garante que qualquer CPF de 11 dígitos e candidato da lista fixa funcionam."""
    repo = AsyncMock()
    repo.get_by_cpf.return_value = None
    service = VotacaoService(repo)

    voto = VotoCreate(cpf=cpf, candidato_numero=candidato_num)
    await service.registrar_voto(voto)

    # Busca o ID correspondente ao número sorteado
    expected_id = next(
        c["id"] for c in CANDIDATOS_FIXOS if c["numero"] == candidato_num
    )
    repo.create_by_id.assert_called_once_with(cpf=cpf, candidato_id=expected_id)


@settings(max_examples=50, deadline=None)
@given(
    cpf=st.from_regex(r"^\d{11}$", fullmatch=True),
    # Gera números que NÃO estão na lista de candidatos
    candidato_num=st.integers(min_value=0, max_value=1000).filter(
        lambda n: n not in [c["numero"] for c in CANDIDATOS_FIXOS]
    ),
)
@pytest.mark.asyncio
async def test_hypothesis_candidato_invalido(cpf, candidato_num):
    """Garante que qualquer número fora da lista fixa lança 400."""
    repo = AsyncMock()
    service = VotacaoService(repo)

    voto = VotoCreate(cpf=cpf, candidato_numero=candidato_num)
    with pytest.raises(HTTPException) as exc:
        await service.registrar_voto(voto)
    assert exc.value.status_code == 400
    repo.create_by_id.assert_not_called()
