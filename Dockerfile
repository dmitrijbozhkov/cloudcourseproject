FROM continuumio/miniconda3
RUN mkdir /cloudcourseproject
WORKDIR /cloudcourseproject
ADD . /cloudcourseproject/
USER root
RUN apt-get update --fix-missing && apt-get install -y nginx redis-server supervisor
RUN pip install -r requirements.txt
RUN conda config --append channels conda-forge
RUN conda install uwsgi libiconv
RUN python -m pytest /cloudcourseproject/tests/
EXPOSE 80 443

CMD ["/usr/bin/supervisord", "-c", "/cloudcourseproject/supervisord.conf"]