# Usamos una imagen liviana y oficial de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero el archivo de requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias necesarias de Python (como Flask y mysql-connector)
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código fuente del backend al contenedor
COPY . .

# Exponemos el puerto en el que corre la aplicación Flask
EXPOSE 5000

# Comando por defecto para ejecutar tu servidor backend
CMD ["python", "Main.py"]