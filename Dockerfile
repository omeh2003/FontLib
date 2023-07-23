#  образ на основе Ubuntu.
FROM ubuntu:latest

#  переменные окружения, чтобы предотвратить взаимодействие с пользователем.
ENV DEBIAN_FRONTEND=noninteractive TZ=Europe/Moscow

# нужные пакеты.
RUN apt-get update && apt-get install -y \
    fontforge \
    python3-full \
    python3-pip \
    python3-fontforge \
    fontforge-extras && \
    rm -rf /var/lib/apt/lists/* &&\
    rm -rf /var/cache/apt/archives/* &&\
    rm -rf /usr/share/doc/* &&\
    apt-get clean

# файл requirements.txt в контейнер.
COPY requirements.txt ./



#  зависимости из requirements.txt.
RUN pip3 install -r requirements.txt

# запуск Python3 по умолчанию.
RUN ln -s $(which python3) /usr/local/bin/python

#  рабочая директория

COPY ./my_generate.py /app/
WORKDIR /app/

# Run your application
CMD ["python", "./my_generate.py"]