FROM python:3.8

ENV APP_ROOT /dojopuzzles

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

EXPOSE 8100

COPY start_app.sh requirements ${APP_ROOT}/
RUN pip install -r ${APP_ROOT}/requirements

ADD dojopuzzles/ ${APP_ROOT}

CMD ["gunicorn", "--bind", "0.0.0.0:8100", "dojopuzzles.wsgi"]
