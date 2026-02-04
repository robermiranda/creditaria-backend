# 1. Usar imagen base oficial ligera de Python
FROM python:3.11.2-alpine

# 2. Establecer directorio de trabajo dentro del contenedor
WORKDIR /code

# 3. Instalar dependencias primero (aprovecha la caché de Docker)
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 4. Copiar los archivos del proyecto al contenedor
# Copia la carpeta app, la carpeta public y main.py
COPY ./app /code/app
COPY ./public /code/public
COPY ./main.py /code/main.py

# 5. Exponer el puerto que utilizará FastAPI
EXPOSE 8000

# 6. Comando para ejecutar la aplicación con Uvicorn
# Se asume que en main.py tienes: app = FastAPI()
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["fastapi", "run", "main.py", "--port", "8000"]
