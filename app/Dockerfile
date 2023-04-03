FROM node:18-bullseye AS node_step

WORKDIR /srv/web/
COPY ./frontend /srv/web/
RUN cd /srv/web \
 && npm install \
 && npm run build

FROM python:3.9.15-slim-buster

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y \
        libgdk-pixbuf2.0-0 \
        libmagic1 \
        libcairo2 \
        libpango-1.0-0 \
        gcc \
        graphviz \
        git \
        locales \
    && pip install --upgrade pip \
    && sed -i '/nl_NL.UTF-8/s/^# //g' /etc/locale.gen && \
        locale-gen

ENV LANG=nl_NL.UTF-8 \
    LANGUAGE=nl_NL \
    LC_ALL=nl_NL.UTF-8

COPY . /app/


RUN mkdir -p /media && mkdir -p /static && chown 2000 /media && chown 2000 /static && chmod 744 /media && chmod 744 /static \
    && mkdir -p /srv/web/var/cache && chown 2000 /srv/web/var/cache && chmod -R ugo+rwx /srv/web/var/cache \
    && chmod +x /app/deploy/docker-entrypoint.sh && chown root:root /app/deploy/docker-entrypoint.sh \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY --from=node_step /srv/web/public/build /static/

CMD ["bash", "/app/deploy/docker-entrypoint.sh"]
