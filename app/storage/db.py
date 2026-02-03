from sqlmodel import select, create_engine, Session
from collections.abc import Sequence
from app.storage.models import Amortizaciones, Anualidades, Auditoria, SelectAnualidades
from functools import lru_cache
from typing import Any
from config import Settings
from ..lib.external import ScoringRiesgo


@lru_cache()
def get_settings():
    return Settings() # type: ignore

settings = get_settings()
engine = create_engine(settings.database_url)


def recupera_tabla_amortizacion (id_grupo: str) -> Sequence[Amortizaciones]:
	"""
	recupera la tabla de amortización dado el id_grupo
	
	:param id_grupo: identidicador de la tabla
	:type id_grupo: str
	"""

	with Session(engine) as session:
		statement = select(Amortizaciones).where(Amortizaciones.id_grupo == id_grupo)
		amortizaciones = session.exec(statement)
		return amortizaciones.all()


def persiste_tabla_amortizacion (
		monto: float,
		tasa_anual: float,
		plazo_meses: float,
		nombre_identificador: str,
		id_grupo: str,
		tabla_amortizacion: list[tuple[int, float, float, float, float]] ):
	
	"""
	Inserta la tabla de amortización en base de datos
	"""
	
    # A la anualidad "a" también se le llama termino de amortización
	termino_amortizacion: float = tabla_amortizacion[1][1]
	
    # Un identificador para relacionar a todas las tuplas de la tabla de amortización

	with Session(engine) as session:
		amortizaciones = []
		for row in tabla_amortizacion:
			amortizacion = Amortizaciones(
				periodo=row[0],
				interes=row[2],
				amortizacion=row[3],
				capital=row[4],
				id_grupo=id_grupo)
			
			amortizaciones.append(amortizacion)
		
		session.add_all(amortizaciones)
		anualidad = Anualidades(
			anualidad=termino_amortizacion,
			monto=monto,
			tasa_anual=tasa_anual,
			plazo_meses=plazo_meses,
			nombre_identificador=nombre_identificador,
			id_grupo=id_grupo)
		
		session.add(anualidad)
		session.commit()
		session.refresh(anualidad)



def recupera_auditoria (id_grupo: str) -> Auditoria | None:
	"""
	recupera la auditoria dado el id_grupo
	
	:param id_grupo: identificador de grupo
	:type id_grupo: str
	"""

	with Session(engine) as session:
		statement = select(Auditoria).where(Auditoria.id_grupo == id_grupo)
		auditoria = session.exec(statement)
		return auditoria.first()
	

def persiste_auditoria_riesgo(id_grupo: str, scoring: ScoringRiesgo):
	"""
	Inserta en base de datos el resultado de la Auditoria de Riesgo
	"""
	
	auditoria = Auditoria(
		umbral=scoring.umbral,
		delay=scoring.delay,
		randomVal=scoring.randomVal,
		valida=scoring.valida,
		id_grupo=id_grupo)
	
	with Session(engine) as session:
		session.add(auditoria)
		session.commit()
		session.refresh(auditoria)
		

def recupera_anualidades (identificador: str):
	"""
	recupera la auditoria dado el id_grupo
	
	:param id_grupo: identificador de grupo
	:type id_grupo: str
	"""

	with Session(engine) as session:
		statement = select(SelectAnualidades).where(SelectAnualidades.nombre_identificador == identificador)
		anualidad = session.exec(statement)
		return anualidad.first()

def recupera_datos_amortizacion_from_db (identificador: str)-> dict[str, Any] | None:
	
	anualidad: SelectAnualidades | None = recupera_anualidades(identificador)
	
	if anualidad is None:
		return None
	
	amortizaciones: Sequence[Amortizaciones] = recupera_tabla_amortizacion(anualidad.id_grupo)
	
	auditoria: Auditoria | None = recupera_auditoria(anualidad.id_grupo)

	if auditoria is None:
		return None
	
	resultado = {
		"amortizaciones": amortizaciones,
		"anualidad": anualidad,
		"auditoria": auditoria
	}

	return resultado