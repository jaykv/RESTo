FROM python:3.9

WORKDIR /usr/local/endpoint

COPY ./requirements.txt /usr/local/endpoint/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /usr/local/endpoint/requirements.txt

COPY ./app /usr/local/endpoint/app

CMD ["gunicorn", "--conf", "app/gunicorn.conf.py", "--bind", "0.0.0.0:5000", "app.run:app"]