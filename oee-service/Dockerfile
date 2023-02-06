# Build the service from the base image
FROM python:3.9.16-alpine3.17

# During building, run the following commands to install dependecies
RUN apk --no-cache add openssl-dev curl curl-dev gcc g++ libgcc
RUN pip install --upgrade pip
RUN pip install pycurl crate requests python-dotenv

# Set the work directory
WORKDIR /oee-service

# Copy in the continer the following files
COPY ./ ./

# Run this command at startup
CMD ["python3","-u","oee_service.py"]