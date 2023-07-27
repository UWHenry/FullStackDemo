FROM node:16-alpine

# Create a non-root user
RUN addgroup -S myusergroup && adduser -S myuser -G myusergroup

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

USER myuser

CMD ["npx", "serve", "-s", "build", "-l", "3000"]
