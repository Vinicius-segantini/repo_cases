# Use uma imagem base do Python
FROM python:3.12.4

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o conteúdo do diretório /src para o contêiner
COPY src/ .

# Exponha a porta em que a API irá rodar
EXPOSE 8080

# Comando para iniciar a API usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]