from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.lib.amortizacion import calcula_tabla_amortizacion
from app.background.tasks import todo_in_background
from app.storage.db import recupera_datos_amortizacion_from_db
from typing import Any
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os


class Prestamo(BaseModel):
	monto: float
	tasa_anual: float
	plazo_meses: int
	nombre_identificador: str | None


app = FastAPI()

#origins = [
#	"http://localhost:5173",
#	"http://localhost:5173/identificador",
#]
#
#app.add_middleware (
#	CORSMiddleware,
#	allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'public')

app.mount("/public", StaticFiles(directory=STATIC_DIR), name="public")

@app.get("/", response_class=HTMLResponse)
async def serve_creditaria_app():
	with open(os.path.join(STATIC_DIR, 'index.html'), 'r') as f:
		return f.read()
	

@app.get(
		"/identificador/{identificador}",
		summary="Obtiene la tabla de amortización",
		description="""
			Obtiene la tabla de Amortización de la base de datos;
			para lo cual es necesario proporcionar el identificador
			de la tabla. Los datos obtenidos se recuperan de la
			base de datos.
		""")
async def recuperaTablaAmortizacion(identificador: str) -> dict[str, Any] | None:

	if identificador is None:
		return None
	
	tabla_amortizacion_y_datos: dict[str, Any] | None = recupera_datos_amortizacion_from_db(identificador)

	return tabla_amortizacion_y_datos


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)