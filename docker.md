1. **docker ps** - List all running containers
2. **docker ps -a** - List all containers  (include stopped containers)
3. **docker rm <container-name> or <container-id>** - Remove a container (Need to stop container first)
4. **docker stop <container-name> or <container-id>** - Stop a container
5. **docker stop $(docker ps -q)** - Stop all running containers
6. **docker images** - List all images
7. **docker rmi <image-name> or <image-id>** - Remove an image


# Steps to fix container error

Run **docker ps** to check for running containers

Run **docker ps -a** to check for stopped containers

Run **docker stop brain-ai-api** to stop a container

Run **docker rm brain-ai-api** to remove a container
