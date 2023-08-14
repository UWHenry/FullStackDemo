# Stage 1: Build the application
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

# Stage 2: Create a production-ready image
FROM node:20-alpine

# Create a non-root user
RUN addgroup -S myusergroup && adduser -S myuser -G myusergroup

WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules

USER myuser

CMD ["npx", "serve", "-s", "build", "-l", "3000"]