# Project README
This README provides instructions and information for setting up and running the project. The project uses Docker Compose to orchestrate the deployment of multiple services, including a Flask backend, a React frontend, a PostgreSQL database, and Nginx for routing.

## Table of Contents
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Technologies Used](#technologies-used)
* [Project Structure](#project-structure)

## Prerequisites
Before you proceed, make sure you have the following installed on your machine:
* Docker & Docker Compose: https://www.docker.com/get-started
  
## Installation
1. Clone the repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2. Build and start the services using Docker Compose:
   ```bash
   docker compose up -d
   ```

## Usage
Once the services are up and running, you can access the application through a web browser.
* Backend API: https://localhost:8443/api/
* Swagger API documentation: https://localhost:8443/api/swagger
* Frontend: https://localhost:8443 (served through Nginx)

## Technologies Used
* Flask: Backend framework for building the API.
    * JWT authentication and CSRF protection are implemented using Flask-JWT-Extended.
    * All REST API endpoints except signup, login, and logout require jwt and csrf validation.
    * Heartbeat websocket is implemented using Flask-SocketIO.
    * Flask-SQLAlchemy is used as the ORM, which automatically handles transactions with each request.
    * Swagger is generated using Flask-RESTX.
* React: Frontend library for building user interfaces.
    * Axios is used for communicating with the backend along with axios-retry for automatic request retries.
    * React Bootstrap is used for consistent and responsive styling.
    * Implements dynamic routing with react-router-dom.
    * Utilizes socket.io-client to implement consume heartbeat websocket from backend.
* PostgreSQL: Database management system.
* Nginx: Web server and reverse proxy server.

## Project Structure
* backend/: Contains the Flask backend application.
* frontend/: Holds the React frontend application.
* nginx/: Contains Nginx configuration files.
* docker-compose.yml: Defines the services and their configurations.