FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "app:app", "-c", "conf.py"]