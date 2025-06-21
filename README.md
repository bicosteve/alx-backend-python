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