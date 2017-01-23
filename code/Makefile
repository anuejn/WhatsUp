default: dev

dev:
	docker-compose -f dev.yml up --build -d

deploy:
	DOCKER_TLS_VERIFY=1 \
	DOCKER_HOST=tcp://212.47.231.85:2376 \
	DOCKER_CERT_PATH=/home/jaro/.docker/machine/machines/deploy \
	DOCKER_MACHINE_NAME=deploy \
	docker-compose -f deploy.yml up --build -d

clean:
	docker-compose -f dev.yml down --remove-orphans

count:
	cloc --exclude-dir=lib --exclude-lang=XML .
