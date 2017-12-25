FROM tensorflow/tensorflow-gpu:latest
MAINTAINER me <me@abc.com>

# httpdのインストール
RUN apt-get install -y 
ホストのindex.htmlをImage内にコピー
ADD ./index.html /var/www/html/

#runした時にapache起動
CMD echo "This is docker-azurflow..."
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
