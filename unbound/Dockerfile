FROM debian:12-slim

RUN apt-get update && apt-get install -y \
    unbound \
    unbound-anchor \
    dnsutils \
    tcpdump \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/unbound /var/lib/unbound

COPY unbound.conf /etc/unbound/unbound.conf
COPY root.hints /etc/unbound/root.hints

EXPOSE 53/udp
EXPOSE 53/tcp

CMD sh -c "unbound-anchor -a /var/lib/unbound/root.key && unbound -d -c /etc/unbound/unbound.conf"
