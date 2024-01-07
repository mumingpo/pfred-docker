FROM continuumio/miniconda3:23.9.0-0

COPY ./pfred-django-backend /home/pfred

WORKDIR /home/pfred

RUN bash ./startup.sh

WORKDIR /home/pfred/django

ENV \
    PFRED_HOME=/home/pfred \
    SCRIPTS_DIR=/home/pfred/scripts/pfred \
    RUN_DIR=/home/pfred/scratch \
    BOWTIE_HOME=/home/pfred/scripts/bowtie \
    BOWTIE=/home/pfred/scripts/bowtie/bowtie \
    BOWTIE_INDEXES=/home/pfred/scripts/bowtie/indexes \
    BOWTIE_BUILD=/home/pfred/scripts/bowtie/bowtie-build \
    PERL5LIB=/home/pfred/scripts/pfred

ENTRYPOINT [ "conda", "run", "-p", "/home/pfred/env", "--no-capture-output", "bash", "./run_development_server.sh" ]
