from fastapi import APIRouter, status
from app.domains.votacao.schema import VotoCreate, CandidatoResponse, ResultadoResponse
from app.domains.votacao.service import VotacaoServiceDep

router = APIRouter(tags=["Votação"])


@router.get("/candidatos", response_model=list[CandidatoResponse])
async def listar_candidatos(service: VotacaoServiceDep):
    """Retorna a lista fixa de candidatos."""
    return service.listar_candidatos()


@router.post("/votos", status_code=status.HTTP_201_CREATED)
async def registrar_voto(voto_data: VotoCreate, service: VotacaoServiceDep):
    """Registra uma intenção de voto."""
    await service.registrar_voto(voto_data)
    return {"message": "Voto registrado com sucesso"}


@router.get("/resultados", response_model=ResultadoResponse)
async def obter_resultados(service: VotacaoServiceDep):
    """Retorna o total de votos e percentuais por candidato."""
    return await service.obter_resultados()
