from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Voto(Base):
    __tablename__ = "votos"

    cpf: Mapped[str] = mapped_column(
        String(11), unique=True, nullable=False, index=True
    )
    candidato_id: Mapped[int] = mapped_column(Integer, nullable=False)
