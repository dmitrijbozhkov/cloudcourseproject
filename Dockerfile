FROM continuumio/miniconda3

RUN mkdir /project
WORKDIR /project
ADD . /project/
RUN pip install -r requirements.txt
RUN python -m pytest tests/

EXPOSE 5000
CMD ["python", "/project/src/app.py"]