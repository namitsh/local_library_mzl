# development Dockerfile

# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/locallibrary

# set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#copy app.sh
# COPY PROJECTS

COPY . .

ENTRYPOINT ["/usr/src/locallibrary/app.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]