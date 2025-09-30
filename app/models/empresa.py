from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

@table_registry.mapped_as_dataclass
class Empresa():
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(init = False, primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cnpj: Mapped[str] = mapped_column(unique=True, nullable=False)
    cidade: Mapped[str] = mapped_column(nullable=False)
    ramo_atuacao: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=False)
    email_contato: Mapped[str] = mapped_column(unique=True, nullable=False)
    data_cadastro: Mapped[datetime] = mapped_column(init=False, server_default=func.now())