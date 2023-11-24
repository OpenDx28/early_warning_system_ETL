# Usa una imagen base de Python 3.9
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos desde el host al contenedor
COPY main.py connection.py etl.py etl_functions.py get_info.py datacon.csv dataorg.csv  /app/

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instala las bibliotecas necesarias
RUN pip install -r requirements.txt

# Comando por defecto para ejecutar el contenedor
CMD ["tail", "-f", "/dev/null"]
