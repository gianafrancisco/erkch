FROM python:3.7-buster

LABEL org.opencontainers.image.authors="gianafrancisco@gmail.com"

ARG USERNAME="user"
ARG UID=1000
ARG GID=1000

ADD requirements.txt /


RUN groupadd -g ${GID} ${USERNAME} && \
    useradd -u ${UID} -g ${GID} ${USERNAME} && \
    python3 -m pip install -r /requirements.txt

USER ${USERNAME}
WORKDIR /src/

EXPOSE 8080
