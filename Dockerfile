FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home/src

COPY ./src /home/src
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
