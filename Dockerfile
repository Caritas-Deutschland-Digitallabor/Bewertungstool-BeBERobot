FROM python:3.9
WORKDIR /app
RUN export DEBIAN_FRONTEND=noninteractive \
 && apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --fix-missing postgresql-client-13 postgresql-client-common \
 && apt-get clean
COPY ./backend /app/backend
COPY ./backup /app/backup
COPY ./db.sqlite /app
COPY ./manage.py /app
COPY ./polls_cms_integration /app/polls_cms_integration
COPY ./requirements.in /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
CMD uwsgi --http=0.0.0.0:80 --module=backend.wsgi
