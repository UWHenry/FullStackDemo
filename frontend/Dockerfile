FROM node:16-alpine

# Create a non-root user
RUN addgroup -S myusergroup && adduser -S myuser -G myusergroup

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL $REACT_APP_API_URL

COPY . .

RUN npm run build

COPY certificates/certificate.crt certificates/private.key /app/certificates/
RUN chown -R myuser:myusergroup /app/certificates/
USER myuser

CMD ["npx", "serve", "-s", "build", "-l", "3000", "--ssl-cert", "certificates/certificate.crt", "--ssl-key", "certificates/private.key"]