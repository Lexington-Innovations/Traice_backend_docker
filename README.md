#Traice_backend

Requirements:
Python3.7 and greater installed

Step 1: Clone this repository

Step 2: Open the terminal in this directory and run the following command: pip install -r requirements.txt

step 3: python3 'flaskapp copy.py'

The flask backend application is up and running on localhost:5005


# Traice_backend_docker

step 1: Make sure your docker instance is running

step 2: Run the command in the current directory terminal:-> docker build -t sample:dev2 .
        {Include the period after dev2}

step 3: Run the next command to run the docker file:-> 
docker run \
    -it \
    --rm \
    -v ${PWD}:/app \
    -v /app/node_modules \
    -p 5005:5005 \
    -e CHOKIDAR_USEPOLLING=true \
   sample:dev2

Docker app is up and running.

