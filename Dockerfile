FROM ubuntu:latest
MAINTAINER Juan Diaz "juan.diaz@dinocloudconsulting.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

######
# Clone and install the application
######
RUN mkdir -p /opt/backend
ADD source  /opt/backend/
WORKDIR /opt/backend
# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt
# Run the application
ENTRYPOINT ["python"]
CMD ["application.py"]