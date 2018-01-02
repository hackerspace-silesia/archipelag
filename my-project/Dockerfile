FROM node
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
VOLUME /usr/src/app
COPY . .
EXPOSE 8080
RUN yarn install
CMD yarn run dev
