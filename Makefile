stop_services:
	systemctl stop postgresql.service
	systemctl stop redis-server.service

clean:
	docker rmi local_stalk_app_backend:latest || true

build:
	docker-compose -f 'docker-compose-local.yml' build

down-containers:
	docker-compose -f 'docker-compose-local.yml' down -v --remove-orphans

up:
	docker-compose -f 'docker-compose-local.yml' up

rs:
	docker exec -it local_stalk_app_redis redis-cli

pg:
	docker exec -it local_stalk_app_postgres psql -U postgres

prune:
	docker system prune -f
	docker volume prune -f
	docker network prune -f
	docker container prune -f
	docker-compose -f 'docker-compose-local.yml' down -v --remove-orphans

all: stop_services prune clean build up