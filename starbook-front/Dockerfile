FROM busybox

MAINTAINER ops@yotpo.com

# Nginx
RUN mkdir -p /etc/nginx/yotpo
COPY nginx/nginx.conf /etc/nginx/yotpo/
VOLUME /etc/nginx/yotpo

# Files
RUN mkdir -p /yotpo/starbook
COPY ./ /yotpo/starbook/
VOLUME /yotpo/starbook

CMD [ "echo", "Find Your boss!" ]