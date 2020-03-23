# Omicron-API

# Introduction

These API endpoints were created as part of a project for managing vulnerabilities in information systems and allow network inventory, scanning and searching for vulnerabilities from a resource https://vulners.com

# REST API

The REST API to the example app is described below.

## Network Inventory

### Request

`POST /api/v1/process/inventory/start`

curl -i -H 'Accept: application/json' http://localhost:5000/api/v1/process/inventory/start

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2020 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    4527bdc9-185c-4db1-9566-b1533685361d
    
## Network Scanner

### Request

`POST /api/v1/process/scanner/ip/start`

curl -i -H 'Accept: application/json' -d 'target=192.168.100.1' http://localhost:5000/api/v1/process/scanner/ip/start

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2020 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    0b9c75fe-0b0a-4761-96c1-7edec91d2364
    
## Network Full Scanner

### Request

`POST /api/v1/process/scanner/full/start`

curl -i -H 'Accept: application/json' -d 'target=192.168.100.0/24' http://localhost:5000/api/v1/process/scanner/ip/start

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2020 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    fe8ff25b-dc53-4685-9f65-1cff1467873f
    
## Result

### Request

`POST /api/v1/result/<uuid>`

curl -i -H 'Accept: application/json' http://localhost:5000/api/v1/result/4527bdc9-185c-4db1-9566-b1533685361d

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2020 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
    "status": [
        "success",
        [
            "192.168.100.4",
            "192.168.100.1"
        ]
    ]
}