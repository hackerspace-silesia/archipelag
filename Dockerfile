FROM frontend
RUN yarn build

FROM hssilesia/archipelag

RUN mkdir /django-static/
RUN python manage.py collectstatic --noinput

FROM kyma/docker-nginx

COPY --from=0 /usr/src/app/dist /var/www
COPY --from=1 /django-static /django-static-files
RUN mv /django-static-files /var/www/django-static

CMD nginx