FROM node:lts-alpine


WORKDIR /front_vue

RUN npm install -g npm

COPY ./ShopFrontVue .
COPY ./ShopFrontVue/front/package*.json /front/package*.json
COPY ./ShopFrontVue/entrypoint.sh  /front_vue/entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh","entrypoint.sh" ]