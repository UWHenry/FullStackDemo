# Base image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package.json package-lock.json ./

# Install project dependencies
RUN npm install

# Copy all the files from the current directory to the container
COPY . .

# Build the React app for production (adjust the build command as needed)
RUN npm run build

# Set the command to run the React app (this assumes your app uses a server like 'serve' to serve the build files)
CMD ["npx", "serve", "-s", "build", "-l", "3000"]

# Expose the port on which the React app will be served (optional, as you'll map the port later when running the container)
EXPOSE 3000
