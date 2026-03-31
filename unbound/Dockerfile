FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG UNBOUND_VERSION=1.19.3

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    dnsutils \
    libevent-dev \
    libssl-dev \
    python3 \
    python3-dev \
    python3-redis \
    swig \
    tcpdump \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN wget "https://www.nlnetlabs.nl/downloads/unbound/unbound-${UNBOUND_VERSION}.tar.gz" && \
    tar xzf "unbound-${UNBOUND_VERSION}.tar.gz" && \
    cd "unbound-${UNBOUND_VERSION}" && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ./configure --with-pythonmodule --with-pyunbound --with-libevent && \
    make -j"$(nproc)" && \
    make install && \
    ldconfig && \
    cd /opt && \
    rm -rf "/opt/unbound-${UNBOUND_VERSION}" "/opt/unbound-${UNBOUND_VERSION}.tar.gz"

RUN mkdir -p /usr/local/etc/unbound /var/lib/unbound /opt/unbound

COPY unbound.conf /usr/local/etc/unbound/unbound.conf
COPY root.hints /usr/local/etc/unbound/root.hints
COPY local-zones.conf /usr/local/etc/unbound/local-zones.conf
COPY redis_pythonmod.py /opt/unbound/redis_pythonmod.py

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["/bin/sh", "-c", "/usr/local/sbin/unbound-anchor -a /var/lib/unbound/root.key && /usr/local/sbin/unbound -d -c /usr/local/etc/unbound/unbound.conf"]
