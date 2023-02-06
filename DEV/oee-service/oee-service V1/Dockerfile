#Specifying the base image
# FROM python:3.8.10
# FROM python:3.9
# FROM python:3.9.16
# FROM python:3.9.16-slim
FROM python:3.9.16-alpine3.17


RUN apk add --no-cache openssl-dev curl-dev gcc g++ libgcc 
# RUN apk add --no-cache gcc g++ python python-dev py-pip mysql-dev linux-headers libffi-dev openssl-dev 
RUN pip install --upgrade pip
RUN pip install pycurl crate requests
#Here we installed the dependencies, we are using the crate library in our oee_calculator.py file so we have to use the pip command for installing the library

WORKDIR /oee-service
# #Here we added the python file that we want to run in docker and define its location.

COPY ./oee_service.py ./oee_service.py

CMD ["python3","-u","oee_service.py"]
#lastly we specified the entry command this line is simply running python ./oee_calculator.py in our container terminal