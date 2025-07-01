```bash
	0. set up a docker environment

	Objective: containerize the Buliding Robust APIs

	Instructions:

	 Create a Requirements.txt file and freeze all the dependencies in it. Hint

	 Install docker for linux. Wondering how, read here.

	 Create a Dockerfile in the root of your messaging app project.

	 Set up the Dockerfile to:
     Use a base Python image python:3.10.
     Install necessary dependencies from the requirements.txt.
     Copy your app code into the container.
     Expose the port your Django app runs on (default is 8000).

     Build the Docker image using the docker build command.

     Run the image in a container and ensure the app works correctly

     # commands
     docker build -t messaging-app .
     docker run -d -p 8000:8000 messaging-app

     docker ps # get container_id

     # run migration
     docker exec -it <container_id> python manage.py migrate


```

```bash
	1. Use Docker Compose for Multi-Container Setup

	Objective: Learn how to manage multiple services using Docker Compose.

	Instructions:

	    Create a docker-compose.yml file at the root of your messaging_app

	    Define two services:
	        web: for your Django messaging app.
	        db: for a MySQL database.

	    Set up the db service with environment variables (such as MYSQL_USER, MYSQL_DB, MYSQL_PASSWORD).

	    Configure the settings.py Database variable to connect to the MYSQL database service using environment variables. hint

	    Use Docker Compose to build and run the multi-container setup.

	    Verify that the app can interact with the MYSQL database.

	Nb: do not push your environment variables to github. Ensure they are in a .env file


	# build:
	docker compose up --build

	# build-detached:
	docker compose up --build -d

	# stop:
	docker compose down

```

```bash
	2. Persist Data Using Volumes

	Objective: Understand how to use Docker volumes to persist database data.Understand how to use Docker volumes to persist database data.

	Instructions:

	    Modify the docker-compose.yml file to add a volume for the MYSQL service, ensuring that the database data is persisted across container restarts.


```

## Jenkins Section

```bash
	0 Set up pipeline on Jenkins

	Install the git plugin, Pipeline and ShiningPandaPlugin. Hint

    Create a Jenkinsfile pipeline script that pulls the messaging app’s code from GitHub, installs dependencies, runs tests using pytest, and generates a report

    Ensure to add Credentials for GitHub

	Repo:

		GitHub repository: alx-backend-python
		Directory: messaging_app
		File: messaging_app/Jenkinsfile
```

```bash
1. Build Docker image with Jenkins

Objective: building a Docker image for your Django messaging app using Jenkins

Instructions:

    Extend the Jenkins Pipeline Script Jenkinsfile to add stages for building and pushing the Docker image

    After updating the Jenkinsfile in your GitHub repository, go to the Jenkins dashboard and trigger the pipeline manually by clicking on Build Now.

    Monitor the build logs to verify that the Docker image is built and pushed to Docker Hub successfully.

Repo:

    GitHub repository: alx-backend-python
    Directory: messaging_app
    File: messaging_app/Jenkinsfile
```

```bash
2. Set Up a GitHub Actions Workflow for Testing

Objective: Set up github actions for Testing

Instructions:

    Create a .github/workflows/ci.yml file in your messaging app’s repository.

    Configure a GitHub Actions workflow that runs the Django tests on every push and pull request.

    Ensure the workflow installs necessary dependencies and sets up a MySQL database for running tests (e.g., using services in GitHub Actions).

Repo:

    GitHub repository: alx-backend-python
    Directory: messaging_app
    File: messaging_app/.github/workflows/ci.yml
```

```bash
3. Code Quality Checks in GitHub Actions:

Objective: Run Code Quality Checks in GitHub Actions

Instructions:

    Extend your GitHub Actions workflow to include a flake8 check for linting the Django project.

    Fail the build if any linting errors are detected.

    Add a step to generate code coverage reports and upload them as build artifacts.

Repo:

    GitHub repository: alx-backend-python
    Directory: messaging_app
    File: messaging_app/.github/workflows/ci.yml


```
