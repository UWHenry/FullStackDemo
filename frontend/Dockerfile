FROM node:14-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

CMD ["npx", "serve", "-s", "build", "-l", "3000"]

EXPOSE 3000
