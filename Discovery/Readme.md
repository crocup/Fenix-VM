# Install
sudo docker build -t fsec_discovery ./

sudo docker run -it --rm --name fsec_discovery fsec_discovery

or 

sudo docker run -d --name fsec_discovery -p 0.0.0.0:8088:8088 fsec_discovery



# RabbitMQ
docker run --restart=always -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq
# Mongo
docker run --restart=always -d --name mongodb_1 -v mongodata:/data/db -p 0.0.0.0:27017:27017 mongo