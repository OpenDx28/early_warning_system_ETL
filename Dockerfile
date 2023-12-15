# Usa una imagen base de Python 3.9
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia todos los archivos desde el host al contenedor
COPY sist_alerta_temprana /app/sist_alerta_temprana/

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instala las bibliotecas necesarias
RUN pip install -r requirements.txt

# Comando por defecto para ejecutar el contenedor
CMD ["tail", "-f", "/dev/null"]
