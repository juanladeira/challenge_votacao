from pydantic import BaseModel, Field, field_validator
import re


class VotoCreate(BaseModel):
    cpf: str = Field(..., description="CPF com exatamente 11 dígitos numéricos")
    candidato_numero: int = Field(..., description="Número do candidato (ex: 13, 45)")

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        if not re.fullmatch(r"\d{11}", v):
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos")
        return v


class CandidatoResponse(BaseModel):
    nome: str
    numero: int


class ResultadoCandidatoResponse(BaseModel):
    nome: str
    numero: int
    votos: int
    percentual: float


class ResultadoResponse(BaseModel):
    total_votos: int
    candidatos: list[ResultadoCandidatoResponse]
