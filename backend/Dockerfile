FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
RUN mkdir -p /project.egg-info

WORKDIR /code
RUN ln -s /project.egg-info archipelag.egg-info

COPY code/requirements.txt .
RUN pip install -r requirements.txt

COPY code .
RUN python setup.py develop
WORKDIR /code/archipelag

# collect static


CMD bash migrate-and-run.sh

EXPOSE 8000