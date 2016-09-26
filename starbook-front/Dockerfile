FROM busybox

MAINTAINER ops@yotpo.com

RUN mkdir -p /yotpo/starbook

COPY ./ /yotpo/starbook/
VOLUME /yotpo/starbook

CMD [ "echo", "Find Your boss!" ]