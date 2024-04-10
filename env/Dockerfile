# Use the official Ubuntu image
FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y python3-tk && \
    rm -rf /var/lib/apt/lists/*

# Install required Python libraries
RUN pip3 install networkx
RUN pip3 install numpy
RUN pip3 install matplotlib


# Set the working directory
WORKDIR /app

# Copy the mvg Python files into the container
COPY . /app

CMD ["/bin/bash"]