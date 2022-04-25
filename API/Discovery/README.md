# Discovery API

## Quick Start in Ubuntu(Debian)
1. Install Docker: 
``sudo apt install docker.io``
2. Build Docker:
``sudo docker build -t fsec_discovery_api ./``
3. Run Docker:
``sudo docker run --restart=always -d --name fsec_discovery_api -p 0.0.0.0:8088:8088 fsec_discovery_api``