from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import create_engine, Session
from app.lib.amortizacion import calcula_tabla_amortizacion
from app.lib.util import genera_string_aleatorio
from app.lib.external import fetch_scoring_service
from app.storage.models import Amortizaciones, Anualidades
from app.storage.db import persiste_tabla_amortizacion


class Prestamo(BaseModel):
	monto: float
	tasa_anual: float
	plazo_meses: int
	nombre_identificador: str | None

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Hello Creditaria with FastAPI"}


@app.post(
		"/simulate",
		summary="Genera la tabla de amortización (Sistema Francés)",
		description="""
			Genera la tabla de amortización en base al
			monto, tasa anual y plazo a meses.
			El tipo de dato entregado es un array de arrays en donde cada array
			representa un renglón en la tabla de amortización.
			Los datos de cada renglón son los siguientes:
			[periodo o mes, anualidad, Interés, Amortización, Capital]
		""")
async def simulate(prestamo: Prestamo):

	prestamo_dic = prestamo.model_dump()
	tasa_mes = prestamo_dic["tasa_anual"] / 12
	prestamo_dic.update({"tasa_mes": tasa_mes})
	tabla_amortizacion = calcula_tabla_amortizacion(prestamo_dic["monto"], tasa_mes, prestamo_dic["plazo_meses"])
	
	persiste_tabla_amortizacion(prestamo_dic["nombre_identificador"], tabla_amortizacion)
	
	return tabla_amortizacion
