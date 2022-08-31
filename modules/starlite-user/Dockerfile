FROM python:3.9

WORKDIR /usr/local/endpoint

COPY ./requirements.txt /usr/local/endpoint/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /usr/local/endpoint/requirements.txt

COPY ./app /usr/local/endpoint/app

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "app.run:app"]