FROM python:3.11.5-slim
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]