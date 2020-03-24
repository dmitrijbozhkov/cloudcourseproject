FROM continuumio/miniconda3
RUN mkdir /project
WORKDIR /project
ADD . /project/
USER root
RUN apt-get update --fix-missing && apt-get install -y nginx redis-server supervisor
RUN pip install -r requirements.txt
RUN conda config --append channels conda-forge
RUN conda install uwsgi libiconv
RUN python -m pytest /project/tests/
EXPOSE 80 443

CMD ["/usr/bin/supervisord", "-c", "/project/supervisord.conf"]