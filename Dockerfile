FROM python:3.10.6

WORKDIR /src/app
ENV FLASK_APP=app
COPY /app/requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt