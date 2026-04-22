FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY main.py .

# Exponer el puerto para la interfaz web
EXPOSE 8550

# Iniciar la aplicación en modo servidor web
CMD ["python", "-m", "flet", "run", "--web", "--port", "8550", "--host", "0.0.0.0", "main.py"]
