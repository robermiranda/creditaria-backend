import httpx
from fastapi import HTTPException
from pydantic import BaseModel


class ScoringRiesgo(BaseModel):
    umbral: float
    delay: float
    randomVal: float
    valida: bool


async def fetch_scoring_service(umbral: float) -> ScoringRiesgo:
    """
    para simular una Auditoría de riesgo se ha creado una edge function la cual es una función
    lambda que recibe el parámetro umbral el cual representa la probabilidad de fallar.
    La función devuelve un objeto como en el siguiente ejemplo:
    {
        "delay": 1.0288641557513,       // tiempo que tarda la petición [de 1 a 3 segundos]
        "randomVal": 0.253347220790455, // numero aleatorio entre [0, 1]
        "valida": false,                // valida = false si randomVal < umbral; valida = true si randomVal >= umbral
        "umbral": 0.5
    }
    en donde valida es de tipo boolean. Si es true entonces la auditoria es favorable al cliente;
    false si no es favorable
    """
    servicio_externo_scoring_url = f"https://lopmuyyhoesmmirrthzg.supabase.co/functions/v1/sleep-random?umbral={umbral}"

    # Use an async context manager for the httpx client
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(servicio_externo_scoring_url, timeout=10.0)
            response.raise_for_status() # Raise an exception for 4xx/5xx responses
            return ScoringRiesgo(**response.json())
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="External API error")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"A network error occurred: {e}")


async def make_auditoria_de_riesgo() -> ScoringRiesgo:
    UMBRAL: float = 0.1
    scoring: ScoringRiesgo = await fetch_scoring_service(UMBRAL)
    return scoring