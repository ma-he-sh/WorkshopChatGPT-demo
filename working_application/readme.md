# Workshop-chatgpt-demo
## Demo of using OpenAI's chatgpt API

### Getting started
- This demo application implements a simple prompt response webui and a chrome addon demo for external requests

### Setting up locally
#### Requirements:
1. Docker and docker-compose
2. Configure the environment variable
```sh
cp .env.example .env
```
3. Generate certificate and setting up hosts file
```sh
cd cli
./create-cert.sh # will create a certs folder and add key and crt certificate files
./trust-cert.sh  # will make the cetificate trusted by chrome
./setup-hosts.sh # will add the domain to hosts so that webserver can be access locally
```
4. Starting up the webserver
```sh
docker-compose up -d
```
5. If you ever change Dockerfile; Rebuild by
```sh
docker-compose up -d --build
```
6. Goto https://myapp.local
7. Following UI Appear
![alt text](https://raw.githubusercontent.com/ma-he-sh/WorkshopChatGPT-demo/main/working_application/images/uipreview.png "Web Preview")
