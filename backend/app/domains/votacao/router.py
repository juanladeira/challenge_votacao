from http import HTTPStatus
from fastapi import APIRouter
from app.domains.votacao.schema import VotoCreate, CandidatoResponse, ResultadoResponse
from app.domains.votacao.service import VotacaoServiceDep

router = APIRouter(tags=["Votação"])


@router.get(
    "/candidatos",
    response_model=list[CandidatoResponse],
    status_code=HTTPStatus.OK,
    description="Retorna a lista fixa de candidatos com seus nomes e números.",
)
async def listar_candidatos(service: VotacaoServiceDep):
    """Retorna a lista fixa de candidatos."""
    return service.listar_candidatos()


@router.post(
    "/votos",
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.BAD_REQUEST: {"description": "Candidato inexistente"},
        HTTPStatus.CONFLICT: {"description": "Este CPF já registrou um voto"},
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Erro de validação (ex: CPF com menos/mais de 11 dígitos ou formato inválido)"
        },
    },
    description="Registra uma intenção de voto válida por CPF. O CPF deve conter exatamente 11 dígitos numéricos.",
)
async def registrar_voto(voto_data: VotoCreate, service: VotacaoServiceDep):
    """Registra uma intenção de voto."""
    await service.registrar_voto(voto_data)
    return {"message": "Voto registrado com sucesso"}


@router.get(
    "/resultados",
    response_model=ResultadoResponse,
    status_code=HTTPStatus.OK,
    description="Retorna o total de votos computados e o desempenho percentual de cada candidato.",
)
async def obter_resultados(service: VotacaoServiceDep):
    """Retorna o total de votos e percentuais por candidato."""
    return await service.obter_resultados()
