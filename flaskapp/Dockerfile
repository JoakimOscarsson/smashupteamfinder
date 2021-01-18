FROM flaskprod

COPY app/ webserver/uwsgi.ini webserver/start.sh /srv/flask_app/
WORKDIR /srv/flask_app

RUN pip install -r requirements.txt --src /usr/local/src

COPY webserver/nginx.conf /etc/nginx/nginx.conf
RUN chmod +x ./start.sh
CMD ["./start.sh"]
