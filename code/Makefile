default: dev

dev:
	docker-compose -f dev.yml up --build -d

deploy: \
	export DOCKER_TLS_VERIFY=1\
	export DOCKER_HOST=tcp://212.47.231.85:2376\
	export DOCKER_CERT_PATH=/home/jaro/.docker/machine/machines/deploy\
	export DOCKER_MACHINE_NAME=deploy

deploy:
	docker-compose up --build -d

clean:
	docker-compose -f dev.yml down --remove-orphans

