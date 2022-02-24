FROM python:3.7

RUN apt-get -y update && \
    apt-get -y install \
        swi-prolog

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /root/python/wizfood
COPY requirements.txt /root/python/wizfood/

RUN pip3 install -r requirements.txt
COPY . /root/python/wizfood/

RUN export FLASK_ENV=staging
RUN export ENV=staging
RUN export FLASK_APP=app
RUN export PYTHONPATH=.

CMD ["gunicorn", "-w", "2", "app:app"]