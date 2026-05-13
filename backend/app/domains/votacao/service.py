from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.domains.votacao.repository import VotacaoRepositoryDep
from app.domains.votacao.schema import (
    VotoCreate,
    CandidatoResponse,
    ResultadoResponse,
    ResultadoCandidatoResponse,
)

CANDIDATOS_FIXOS = [
    {"id": 1, "nome": "Maria Silva", "numero": 13},
    {"id": 2, "nome": "João Souza", "numero": 45},
]


class VotacaoService:
    def __init__(self, repository: VotacaoRepositoryDep):
        self._repository = repository

    def listar_candidatos(self) -> list[CandidatoResponse]:
        return [CandidatoResponse(**c) for c in CANDIDATOS_FIXOS]

    async def registrar_voto(self, voto_data: VotoCreate) -> None:
        # 1. Validar se o candidato existe pelo NÚMERO
        candidato = next(
            (c for c in CANDIDATOS_FIXOS if c["numero"] == voto_data.candidato_numero),
            None,
        )
        if not candidato:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Candidato inexistente"
            )

        # 2. Validar se o CPF já votou
        voto_existente = await self._repository.get_by_cpf(voto_data.cpf)
        if voto_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este CPF já registrou um voto",
            )

        # 3. Registrar o voto usando o ID interno para consistência no banco
        await self._repository.create_by_id(
            cpf=voto_data.cpf, candidato_id=candidato["id"]
        )

    async def obter_resultados(self) -> ResultadoResponse:
        votos_por_candidato = await self._repository.get_vote_counts()
        total_votos = sum(votos_por_candidato.values())

        candidatos_resultado = []
        for c in CANDIDATOS_FIXOS:
            votos = votos_por_candidato.get(c["id"], 0)
            percentual = (votos / total_votos * 100) if total_votos > 0 else 0

            candidatos_resultado.append(
                ResultadoCandidatoResponse(
                    nome=c["nome"],
                    numero=c["numero"],
                    votos=votos,
                    percentual=round(percentual, 2),
                )
            )

        return ResultadoResponse(
            total_votos=total_votos, candidatos=candidatos_resultado
        )


def get_votacao_service(repository: VotacaoRepositoryDep) -> VotacaoService:
    return VotacaoService(repository)


VotacaoServiceDep = Annotated[VotacaoService, Depends(get_votacao_service)]
