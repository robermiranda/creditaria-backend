from typing import Any
from app.storage.db import persiste_tabla_amortizacion
from app.lib.external import make_auditoria_de_riesgo
from app.storage.db import persiste_auditoria_riesgo
from app.lib.util import genera_string_aleatorio


async def todo_in_background (
        prestamo: dict[str, Any],
        tabla_amortizacion: list[tuple[int, float, float, float, float]] ) :
    
    id_grupo: str = genera_string_aleatorio(16)

    print('==============> BG: ID GRUPO', id_grupo)

    persiste_tabla_amortizacion(
        prestamo["monto"],
        prestamo["tasa_anual"],
        prestamo["plazo_meses"],
        prestamo["nombre_identificador"],
        id_grupo,
        tabla_amortizacion)
    
    print('==============> BG: SE PERSISTE AMORTIZACION')

    auditoria = await make_auditoria_de_riesgo()

    print('==============> BG: AUDITORIA [DELAY, RANDOMVAL]', auditoria.delay, auditoria.randomVal)

    persiste_auditoria_riesgo(id_grupo, auditoria)

    print('==============> BG: SE PERSISTE AUDITORIO')