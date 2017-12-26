FROM tensorflow/tensorflow:latest-gpu
MAINTAINER me <me@abc.com>

RUN mkdir /app
WORKDIR /app

# httpdのインストール
# RUN apt-get install -y 

#runした時にapache起動
# CMD echo "This is docker-azurflow..."
CMD ["python", "train.py"]
