# Use uma imagem base Python com suporte a SQLite
FROM python:3.12-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de dependência
COPY pyproject.toml poetry.lock ./

# Instale as dependências do projeto
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

# Copie o código fonte da aplicação
COPY . .

# Exponha a porta que a API irá utilizar
EXPOSE 8000

# Comando para iniciar a API
CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]