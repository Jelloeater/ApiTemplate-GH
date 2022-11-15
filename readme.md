[![Python package](https://github.com/Jelloeater/ApiTemplate-GH/actions/workflows/test.yaml/badge.svg)](https://github.com/Jelloeater/ApiTemplate-GH/actions/workflows/test.yaml)

This is a nice template project I cooked up using Drone CI/CD

If you feel like running it yourself, give it a shot!

**docker-compose.yml**
``` yml
version: '3.8'

services:
  registry:
    image: registry:2
    ports:
    - "5000:5000"

  gitea:
    container_name: gitea
    image: gitea/gitea
    restart: unless-stopped
    environment:
      # https://docs.gitea.io/en-us/install-with-docker/#environments-variables
      - APP_NAME="Gitea"
      - USER_UID=1000
      - USER_GID=1000
      - RUN_MODE=prod
      - DOMAIN=local_server_ip_GOES_HERE
      - SSH_DOMAIN=local_server_ip_GOES_HERE
      - HTTP_PORT=3000
      - ROOT_URL=https://gittea.yourdomain.tld
      - SSH_PORT=222
      - SSH_LISTEN_PORT=22
      - DB_TYPE=sqlite3
    ports:
      - "3000:3000"
      - "222:22"
    networks:
      - cicd_net
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro


  drone:
    container_name: drone
    image: drone/drone
    restart: unless-stopped
    depends_on:
      - gitea
    environment:
      # https://docs.drone.io/server/provider/gitea/
      - DRONE_DATABASE_DRIVER=sqlite3
      - DRONE_DATABASE_DATASOURCE=/data/database.sqlite
      - DRONE_GITEA_SERVER=https://gittea.yourdomain.tld
      - DRONE_GIT_ALWAYS_AUTH=false
      - DRONE_RPC_SECRET=correct-horse-batter-staple
      - DRONE_SERVER_PROTO=http
      - DRONE_SERVER_HOST=local_server_ip_GOES_HERE:3001
      - DRONE_TLS_AUTOCERT=false
      - DRONE_USER_CREATE=gittea_username_goes_here
      - DRONE_GITEA_CLIENT_ID=You need to generate this from GitTea
      - DRONE_GITEA_CLIENT_SECRET=SEE https://docs.drone.io/server/provider/gitea/
    ports:
      - "3001:80"
      - "9001:9000"
    networks:
      - cicd_net
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./drone:/data

  drone-runner:
    container_name: drone-runner
    image: drone/drone-runner-docker
    restart: unless-stopped
    depends_on:
      - drone
    environment:
      # https://docs.drone.io/runner/docker/installation/linux/
      # https://docs.drone.io/server/metrics/
      - DRONE_RPC_PROTO=http
      - DRONE_RPC_HOST=drone
      - DRONE_RPC_SECRET=correct-horse-batter-staple
      - DRONE_RUNNER_NAME="drone-runner"
      - DRONE_RUNNER_CAPACITY=2
      - DRONE_RUNNER_NETWORKS=cicd_net
      - DRONE_DEBUG=false
      - DRONE_TRACE=false
    ports:
      - "3002:3000"
    networks:
      - cicd_net
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock



networks:
  cicd_net:
   name: cicd_net

```