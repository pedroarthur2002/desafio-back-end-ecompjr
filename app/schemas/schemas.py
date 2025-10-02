from pydantic import BaseModel, EmailStr, field_validator
from typing import ClassVar
from datetime import datetime


def validar_cnpj(cnpj: str) -> bool:
    cnpj = ''.join(filter(str.isdigit, cnpj))

    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj_base, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj_base, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6] + pesos_1

    digito1 = calcular_digito(cnpj[:12], pesos_1)
    digito2 = calcular_digito(cnpj[:12] + digito1, pesos_2)

    return cnpj[-2:] == digito1 + digito2


class EmpresaBase(BaseModel):
    nome: str
    cidade: str
    ramo_atuacao: str
    telefone: str


class EmpresaCreate(EmpresaBase):
    cnpj: str
    email_contato: EmailStr

    
    @field_validator("cnpj")
    @classmethod
    def cnpj_valido(cls, v: str) -> str:
        if not validar_cnpj(v):
            raise ValueError("CNPJ inválido")
        return v

class EmpresaResponse(EmpresaBase):
    id: int
    data_cadastro: datetime