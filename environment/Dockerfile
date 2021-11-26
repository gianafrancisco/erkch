FROM python:3.7-buster

LABEL org.opencontainers.image.authors="gianafrancisco@gmail.com"

ARG USERNAME="user"
ARG UID=1000
ARG GID=1000

EXPOSE 8080

WORKDIR /src/

ADD requirements.txt /

RUN groupadd -g ${GID} ${USERNAME} && \
    useradd -u ${UID} -g ${GID} ${USERNAME} && \
    python3 -m pip install -r /requirements.txt

ADD app.tar.gz /src/

USER ${USERNAME}

CMD [ "uvicorn", "app.main:app", "--port","8080", "--host", "0.0.0.0" ]
