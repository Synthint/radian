.PHONY: start-rebuild
start-rebuild: # containers are pretty rad
	docker build -t radian:dev . && docker-compose up

.PHONY: build
build:
	docker build -t radian:dev .