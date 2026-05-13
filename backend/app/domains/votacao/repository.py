from typing import Annotated
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncDBSession
from app.domains.votacao.model import Voto


class VotacaoRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_cpf(self, cpf: str) -> Voto | None:
        query = select(Voto).where(Voto.cpf == cpf)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def create_by_id(self, cpf: str, candidato_id: int) -> Voto:
        voto = Voto(cpf=cpf, candidato_id=candidato_id)
        self._session.add(voto)
        await self._session.flush()
        return voto

    async def get_vote_counts(self) -> dict[int, int]:
        """Retorna um dicionário {candidato_id: quantidade_votos}"""
        query = select(Voto.candidato_id, func.count(Voto.id)).group_by(
            Voto.candidato_id
        )
        result = await self._session.execute(query)
        return {row[0]: row[1] for row in result.all()}


def get_votacao_repository(session: AsyncDBSession) -> VotacaoRepository:
    return VotacaoRepository(session)


VotacaoRepositoryDep = Annotated[VotacaoRepository, Depends(get_votacao_repository)]
