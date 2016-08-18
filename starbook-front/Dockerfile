FROM node:4
RUN npm install -g serve
COPY . /var/www/
RUN cd /var/www && npm install
CMD serve -p ${PORT} /var/www
