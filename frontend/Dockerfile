FROM node:8.9.1

ENV APP_DIR /usr/src/app

RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

ADD package.json .
RUN yarn install

ADD . $APP_DIR
EXPOSE 8080

ENV PATH "$PATH:$APP_DIR/node_modules/.bin"
VOLUME $APP_DIR/node_modules

CMD yarn run dev
