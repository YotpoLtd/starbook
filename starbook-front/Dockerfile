FROM node:4
RUN npm install -g serve
COPY . /var/www/
CMD serve -p ${PORT} /var/www
