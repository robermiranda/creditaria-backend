from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from app.lib.amortizacion import calcula_tabla_amortizacion
from app.background.tasks import todo_in_background


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
async def simulate(prestamo: Prestamo, background_tasks: BackgroundTasks):

	prestamo_dic = prestamo.model_dump()
	tasa_mes = prestamo_dic["tasa_anual"] / 12
	prestamo_dic.update({"tasa_mes": tasa_mes})
	tabla_amortizacion = calcula_tabla_amortizacion(prestamo_dic["monto"], tasa_mes, prestamo_dic["plazo_meses"])
	
	background_tasks.add_task (
		todo_in_background,
		prestamo_dic,
		tabla_amortizacion )
	
	print('###############> MAIN: SE RESPONDIENDO LA TABLA DE AMORTIZACIÓN')
	return tabla_amortizacion
