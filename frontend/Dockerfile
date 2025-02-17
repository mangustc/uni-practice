FROM node:23.1.0

WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install

COPY . .
COPY vite.config-docker.ts vite.config.ts

# RUN npm run build

#COPY ./dist /html

# CMD [ "cp", "-rfva", "/app/dist/.", "/html"]
CMD [ "npm", "run", "dev" ]
EXPOSE 5173
