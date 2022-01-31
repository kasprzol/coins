FROM python:3.10

RUN python3 -m pip install -U pip wheel
RUN mkdir -p /srv/coins
WORKDIR /srv/coins
COPY .. /srv/coins
RUN pip install .

ENV deployment=production

ENTRYPOINT ["/srv/coins/docker/webapp_entrypoint.sh"]

