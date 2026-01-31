from sqlmodel import SQLModel, Field, Relationship
#from typing import Optional, List


class Amortizaciones(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    periodo: int
    interes: float
    amortizacion: float
    capital: float
    id_grupo: str


class Anualidades (SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    #created_at: str | None = Field(default=None, nullable=True)
    anualidad: float
    aprobado: bool | None = None
    nombre_identificador: str | None = None
    id_grupo: str



class Auditoria (SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    umbral: float
    delay: float
    randomVal: float
    valida: bool
    id_grupo: str
