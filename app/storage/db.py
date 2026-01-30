from app.lib.util import genera_string_aleatorio
from sqlmodel import create_engine, Session
from app.storage.models import Amortizaciones, Anualidades
from functools import lru_cache
from config import Settings


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
print('DATA BASE URL FROM .ENV', settings.database_url)
engine = create_engine(settings.database_url, echo=True)

def persiste_tabla_amortizacion (
		nombre_identificador: str,
		tabla_amortizacion: list[tuple[int, float, float, float, float]] ):
	
	"""
	Inserta la tabla de amortización en base de datos
	"""
	
    # A la anualidad "a" también se le llama termino de amortización
	termino_amortizacion: float = tabla_amortizacion[1][1]
	
    # Un identificador para relacionar a todas las tuplas de la tabla de amortización
	id_grupo = genera_string_aleatorio(16)

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
			nombre_identificador=nombre_identificador,
			id_grupo=id_grupo)
		
		session.add(anualidad)
		session.commit()
		session.refresh(anualidad)
