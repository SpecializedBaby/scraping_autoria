FROM python:3.11-alpine3.21
LABEL maintainer="specialized8393@gmail.com"

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV TZ=UTC

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]