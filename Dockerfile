# 1. Imagen base oficial de Python ligera
FROM python:3.9-slim

# 2. Definir directorio de trabajo
WORKDIR /app

# 3. Copiar requirements primero (para optimizar caché)
COPY ./requirements.txt /app/requirements.txt

# 4. Instalar dependencias
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 5. Copiar el resto del código de la aplicación
COPY . /app

# 6. Exponer el puerto
EXPOSE 8000

# 7. Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
