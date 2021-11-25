FROM python:3.9
WORKDIR /code
COPY ./requirements/base.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY .env /code/.env
COPY server /code/server

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
