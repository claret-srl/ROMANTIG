#Specifying the base image
FROM python:3.8.10

#here the dockerfile is pulling the python 3.10 from docker hub which already has python installed so we have all the things we need to have python in our container.

# #Here we added the python file that we want to run in docker and define its location.
WORKDIR /oee-service

# RUN 

RUN pip install requests crate
#Here we installed the dependencies, we are using the crate library in our oee_calculator.py file so we have to use the pip command for installing the library

COPY . .

# CMD [ "python3", "./oee_service.py" ]
#lastly we specified the entry command this line is simply running python ./oee_calculator.py in our container terminal