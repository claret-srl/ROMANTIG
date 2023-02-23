# Build the service from the base image
FROM python:3.9.16-alpine3.17

# Set the work directory
WORKDIR /app

# During building, run the following commands to update, upgrade and install the required dependecies
RUN 	apk update \
	&&	apk add --upgrade apk-tools \
	&&	apk upgrade \
	&&	apk --no-cache add openssl-dev curl curl-dev gcc g++ libgcc

RUN		pip install --upgrade pip \
	&&	pip install pycurl requests python-dotenv

# Copy in the continer the following files
COPY . .

# Run this command at startup
CMD ["python3", "-u", "main.py"]