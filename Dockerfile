FROM kong/kong-gateway:3.7.1.2-rhel

USER root

COPY requirements.txt /usr/local/bin/dependency/requirements.txt

RUN dnf install -y python3-pip python-devel

RUN pip3 install -r /usr/local/bin/dependency/requirements.txt

RUN python3 -m spacy download en_core_web_trf

COPY /plugin/*.py /usr/local/bin/

RUN chmod a+x /usr/local/bin/*.py

USER kong
