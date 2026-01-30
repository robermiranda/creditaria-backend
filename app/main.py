from fastapi import FastAPI
from pydantic import BaseModel
from app.lib.amortizacion import calcula_tabla_amortizacion
from app.lib.util import genera_string_aleatorio
from sqlmodel import create_engine, SQLModel, Session
from app.storage.models import Amortizaciones, Anualidades


class Prestamo(BaseModel):
	monto: float
	tasa_anual: float
	plazo_meses: int
	nombre_identificador: str | None

DATABASE_URL = "???"
engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI()

@app.get("/")
async def root():
	return {"message": "Hello Creditaria with FastAPI"}


@app.post("/simulate")
async def simulate(prestamo: Prestamo):

	prestamo_dic = prestamo.model_dump()
	tasa_mes = prestamo_dic["tasa_anual"] / 12
	prestamo_dic.update({"tasa_mes": tasa_mes})
	tabla_amortizacion = calcula_tabla_amortizacion(prestamo_dic["monto"], tasa_mes, prestamo_dic["plazo_meses"])
	termino_amortizacion: float = tabla_amortizacion[1][1]
	id_grupo = genera_string_aleatorio(16)

	with Session(engine) as session:
		amortizaciones = []
		for row in tabla_amortizacion:
			amortizacion = Amortizaciones(periodo=row[0], interes=row[2], amortizacion=row[3], capital=row[4], id_grupo=id_grupo)
			amortizaciones.append(amortizacion)
		
		session.add_all(amortizaciones)
		anualidad = Anualidades(anualidad=termino_amortizacion, nombre_identificador=prestamo_dic["nombre_identificador"], id_grupo=id_grupo)
		session.add(anualidad)
		session.commit()
		session.refresh(anualidad)

		print('ANUALIDAD', anualidad)

	return tabla_amortizacion
