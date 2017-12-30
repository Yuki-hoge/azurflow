FROM tensorflow/tensorflow:latest-gpu
MAINTAINER me <me@abc.com>

# working directory of d-azurflow
# mount azurflow directory (../) on here (/app)
RUN mkdir /app
WORKDIR /app

# installation of keras
RUN pip install keras

# the default command that runs when docker container starts
# CMD echo "This is docker-azurflow..."
CMD ["python", "train.py"]
