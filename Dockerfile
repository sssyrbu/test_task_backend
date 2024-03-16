FROM python:3.11.8-alpine3.18

WORKDIR /ref_api

COPY . /ref_api

RUN pip install --no-cache-dir -r requirements.txt

RUN apk add openssl

RUN echo "SECRET_KEY = '$(openssl rand -hex 32)'" >> .env

EXPOSE 8081

CMD ["sh", "-c", "cd app/ && python3 main.py"]
