ARG PHP_IMAGE
FROM ${PHP_IMAGE}
COPY xdebug.tgz /tmp/xdebug.tgz
RUN pecl install /tmp/xdebug.tgz && docker-php-ext-enable xdebug && rm /tmp/xdebug.tgz
COPY phpstan.phar /opt/phpstan.phar
ENV XDEBUG_MODE=off
