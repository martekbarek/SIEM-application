# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables

# disables an automatic check for pip updates each time
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# means Python will not try to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# ensures our console output is not buffered by Docker
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["sh","/usr/src/app/entrypoint.sh"]