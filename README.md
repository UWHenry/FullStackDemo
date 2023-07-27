# technical-assessment
## Unfinished Challenges and Thoughts
* CSRF
    * I tried to implement it on flask and created an api for the frontend to get CSRF token.
    * However, I encountered difficulties in configuring the React frontend to pass the CSRF validation. As a result, I decided to move on to other tasks for the time being, intending to revisit this issue later.
* XSS
    * I believe that cross-site scripting protection is primarily related to frontend development. However, I am uncertain about how to implement this protection from the backend.
    * In my understanding, utilizing an ORM and avoiding raw SQL statements can provide protection against SQL Injection.
* Websocket
    * I am aware that WebSocket facilitates bidirectional communication through a long-lived connection, but I am not familiar with its implementation details.
* Transaction test
    * With optimistic lock, my understanding is that test processes should abandon their changes if they check the version_id and find that it indicates data updates that occurred after they started modifying the data.
    * Using a transaction ensures that all operations within it are treated as a single unit, and if any SQL operation fails, the entire transaction is rolled back. However, my current implementation updates one model at a time, making it difficult to test the full transaction behavior. To perform a comprehensive test, I could create a new transaction that updates both the user and the role models, causing one update to intentionally fail, and then observe the outcome. However, this approach may not fully test the functions that implement transactions.
*  Deployment
    * Integrating React and Flask presented challenges, primarily due to route configurations.
    * I encountered difficulties configuring Nginx to display the Swagger page correctly for the APIs. As a temporary solution, I exposed the backend server's port to access the Swagger page from the browser, although this is not an ideal approach.
    * During the deployment in my Mac development environment, API calls from the frontend to the backend were successful. However, after moving the servers to a remote Ubuntu environment, the API configuration broke, leading to communication failures between the frontend and backend. To address this issue, I intend to conduct an investigation into the server routings and Nginx configuration to pinpoint the root cause of the problem.

## Application Hosting and Environments
* You can start the application using either of the following commands, as they are equivalent:
    ```
    docker compose up -d --build
    ```
    ```
    ./run_docker.sh
    ```
* The frontend can be accessed via ```https://localhost:8443/```, and the swagger can be accessed via ```https://localhost:8000/```
* The deployment commands perform successfully on my Mac and Docker Desktop with Google Chrome, and they are anticipated to work similarly on a Windows environment with Docker Desktop. However, when deploying the application to a remote Ubuntu environment, the communication between the servers breaks, indicating the need for additional investigation and troubleshooting to identify the root cause of the issue.

## Assessments
1. Model is at ```/backend/models/user.py```
2. Functions are at ```/backend/db_utils/user_manager.py```
3. Uses flask-sqlalchemy
4. Models are at ```/backend/models/```
5. Only implement on update, see implementations in ```/backend/db_utils/user_manager.py``` and ```/backend/db_utils/role_manager.py``` in the ```update``` function
6. Wrap transaction in ```delete, update, create``` actions, don't need transactions in ```read```
7. Generated with flask-restx, swagger at ```https://localhost:8000```
8. Enabled via gunicorn
9. Created in ```/backend/resources/user_resource.py``` the ```SignUp``` Resource class
10. Created in ```/backend/resources/user_resource.py``` the ```Login``` Resource class, verify with json web token
11. Created in ```/backend/resources/user_resource.py``` the ```UserResource``` Resource class
12. Same as 11
13. Same as 11
14. Created in ```/backend/resources/user_resource.py```, ```UserSearchResource``` performs conditional query, ```UserListResource``` lists all users
15. Created in ```/backend/resources/role_resource.py```
16. Same as 15
17. Did not implement
18. Did not implement
19. Did not implement
20. Created in ```/backend/resources/db_testing_resource.py``` the ```OptimisticLockTest``` Resource class
21. Did not implement
22. Created in ```/frontent/src/components/sign_page.js```
23. Created in ```/frontend/src/components/login_page.js```
24. Created in ```/frontend/src/components/navigation_menu.js```
25. Created in ```/frontend/src/components/user_list_page.js```
26. Created in ```/frontent/src/components/user_edit_page.js```
27. Created in ```/frontend/src/components/role_list_page.js```
28. Created in ```/frontend/src/components/role_edit_page.js```
29. Did not implement
30. Created in ```/frontend/src/components/optimistic_lock_testing_page.js```
31. Did not implement
32. Created Dockerfile for backend and frontend, build via docker compose
33. Clustered via docker compose
34. Unsuccessful in configuring 
35. Use ```./run_docker.sh```
36. Https certificates are mounted via docker-compose
37. In both the frontend and backend Dockerfiles, implemented the creation and switching to a non-root user just before starting the servers
