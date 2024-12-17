FROM nginx
COPY nginx/config/nginx.conf /etc/nginx/nginx.conf
COPY static /data/static

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
