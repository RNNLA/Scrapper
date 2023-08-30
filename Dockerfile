FROM ubuntu:22.04

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y install tzdata
RUN apt-get -y install python3 \
    python3-pip \
    tor \
    && apt-get clean

WORKDIR /app
COPY . /app
COPY env /etc/tor/torrc
RUN pip install .
RUN service tor start
RUN service tor restart
CMD ["python3", "-m", "scrapper"]
