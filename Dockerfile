FROM continuumio/miniconda3:23.9.0-0

COPY ./pfred-django-backend /home/pfred

WORKDIR /home/pfred

RUN ./startup.sh

SHELL [ "conda", "run", "-n", "/home/pfred/env", "bash", "-c" ]

WORKDIR /home/pfred/django

ENTRYPOINT [ "bash", "./run_development_server.sh" ]
