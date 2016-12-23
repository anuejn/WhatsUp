FROM nginx:latest
COPY default.conf etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html

ARG GIT_COMMIT
RUN sed -i -e "s/#VERSION/${GIT_COMMIT}/" /usr/share/nginx/html/css/version.css
