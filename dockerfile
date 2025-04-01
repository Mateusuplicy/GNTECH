# Usar uma imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta 5000 (porta padrão do Flask)
EXPOSE 5000

# Definir o comando para rodar a aplicação Flask
CMD ["python", "api.py"]
