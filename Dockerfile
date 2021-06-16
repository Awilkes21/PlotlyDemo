# Docker file used to configure the Docker image used for the Example Plotly Dash app
# uses a base UBI redhat image with python 3 support
FROM registry.access.redhat.com/ubi8/python-38:latest
MAINTAINER "You"

# set root user access for container building
USER root

# expose port 8085 for the Dash Flask server
EXPOSE 8085

# install vim for debug editing
RUN yum install vim -y

# create working directory
WORKDIR /plotly_dash
# copy all files
ADD . /plotly_dash

# install required dependencies
RUN pip3 install -r requirements.txt

# set the starting script to the entrypoint.sh script specified at the start of the dockerfile
ENTRYPOINT ["/plotly_dash/entrypoint.sh"]