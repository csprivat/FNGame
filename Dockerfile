# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos para o container
COPY . .

# Instala dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para rodar o bot
CMD ["python", "FNGame-1.4.py"]