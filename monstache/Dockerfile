FROM rwynn/monstache:6.4.3

WORKDIR /pfe

COPY monstache.toml monstache.config.toml

ENTRYPOINT ["/bin/monstache", "-f", "monstache.config.toml"]