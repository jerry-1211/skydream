FROM nginx:1.25-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx-init.conf /etc/nginx/conf.d/nginx-init.conf.bak

EXPOSE 80 443
