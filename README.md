# Example_Plotly_Dash

This repository contains a starting example for a Plotly Dash web application. It is intended for instructional usage and not as an exhaustive source of knowledge or as a solution to any specific problem.

# Docker Build
A Dockerfile is provided within this repository. The Dockerfile is setup to build a container that will automatically deploy the
dash web server. To utilize the Dockerfile to build the example plotly dash app, you will need Docker:

https://docs.docker.com/docker-for-windows/install/

From the command line the following command may be run to build the docker container:

**docker build -t example_plotly_dash .**

**Note you may replace example_plotly_dash with whatever name you want to name the container on your local system**

The web app server currently utilizes port 8050 to serve the web front end connection. It is neccessary to ensure that this port is properly published
when the container image is run. The following command provides the minimum required flags to run the container within docker:

**docker run --publish 8050:8050 example_plotly_dash**

This will run the container which will invoke the entrypoint script to launch the web server. You may then connect any browser to:

**localhost:8050/**

# Run Without Docker
In order to run the example without using docker, that is, to run the example directly on your local machine, you will need to ensure
that all sufficient python required packages are installed. You may do this by utilizing the requirements.txt file provided as part
of the repository. You may simply run:

**pip3 install -r requirements.txt**

to install the packages directly as specified in the requirements.txt, or you may manually install each package or equivalent as you desire.

To then run the web app locally use the following command:

**python example_plotly_app.py**

This will start the webserver on the localhost port 8050 by default. Additional command line arguments may be used as follows:

**-h HOSTIP**
Specifies an ip other than localhost 0.0.0.0

-p HOSTPORT
Specifies a port to use other than 8050

-w NO ARGUMENT
Specifies whether to use Waitress Web Server Gateway Interface, takes no value other than flag

# Trouble Shooting
If you receive an error when running the docker container that includes an error involving:

**'bash\r' not found**

or something to that effect, that means that your git package is set to change line endings on checkout. You want to reconfigure your git
to checkout line endings as is and commit line endings as is to ensure that no additional characters, such as the carriage return '\r' are
added due to cloning the repository down to a Windows OS.