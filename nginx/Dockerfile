FROM nginx:alpine

COPY ./nginx-default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-nginx.conf /etc/nginx/nginx.conf

CMD exec nginx -g 'daemon off;'
