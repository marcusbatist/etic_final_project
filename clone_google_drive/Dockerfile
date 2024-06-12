# Usa a imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /projeto_final/

# Copia os arquivos do projeto para o contêiner
COPY . /app

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto
RUN poetry install

# Exponha a porta que o Django usa (8000 por padrão)
EXPOSE 8000

# Comando para rodar o servidor de desenvolvimento do Django
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
