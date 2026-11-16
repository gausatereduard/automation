FROM composer:2 AS composer

FROM jenkins/ssh-agent

# Install PHP CLI, the extensions required by the project, and Composer
RUN apt-get update && apt-get install -y --no-install-recommends \
        php-cli \
        php-sqlite3 \
        php-mbstring \
        php-xml \
        php-zip \
        unzip \
        git \
        psmisc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer /usr/bin/composer /usr/local/bin/composer
