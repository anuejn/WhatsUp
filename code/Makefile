default: dev

dev:
	docker-compose up --build -d

clean:
	docker-compose -f dev.yml down --remove-orphans

count:
	cloc --exclude-dir=lib --exclude-lang=XML .
