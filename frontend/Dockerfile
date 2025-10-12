FROM node:20

ARG BUILD_MODE=local

WORKDIR /stalk_app/frontend

COPY package*.json .

RUN if [ "$BUILD_MODE" = "prod" ]; then \
	npm install; \
	fi

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]