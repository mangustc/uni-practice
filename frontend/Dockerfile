FROM node:23.1.0

WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install

COPY . .

# RUN npm run build

#COPY ./dist /html

# CMD [ "cp", "-rfva", "/app/dist/.", "/html"]
CMD [ "npm", "run", "dev" ]
EXPOSE 5173
