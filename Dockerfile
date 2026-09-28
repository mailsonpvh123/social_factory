FROM python:3.11-slim

WORKDIR /app

# Instala o FFmpeg e limpa o cache do apt para manter o container leve
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do código para dentro do container
COPY . .

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar o painel web
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
