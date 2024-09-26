DOCKER_IMAGE_NAME=secret-santa-api
DOCKER_CONTAINER_NAME=secret-santa-api-container
PORT=8000

docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .


docker-run:
	docker run -d -p $(PORT):8000 --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)


docker-stop:
	docker stop $(DOCKER_CONTAINER_NAME) || true
	docker rm $(DOCKER_CONTAINER_NAME) || true


docker-clean:
	docker system prune -f


docker-logs:
	docker logs -f $(DOCKER_CONTAINER_NAME)

reload-api: docker-stop docker-build docker-run
	@echo "API reloaded successfully."
