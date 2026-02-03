# Use uma imagem oficial do Python
FROM python:3.12-slim

# Impede que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para o psycopg2 e outras libs
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . /app/

# Coleta os arquivos estáticos (serão servidos pelo Easypanel/Nginx)
# Nota: No Easypanel, o collectstatic pode ser rodado aqui ou no comando de inicialização
RUN python manage.py collectstatic --noinput

# Expõe a porta que o Gunicorn vai rodar
EXPOSE 8000

# Comando para iniciar a aplicação usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
