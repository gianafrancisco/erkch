docker_io_image = "fgiana/eureka-api:latest"
branch = "main"
tests = "tests"

build: git
	docker rmi eureka-api:latest || echo ""
	docker build -f environment/Dockerfile \
	--build-arg USERNAME=${USER} \
	--build-arg UID=$(shell id -u) \
	--build-arg GID=$(shell id -g) \
	-t eureka-api environment

git:
	git archive --format tar.gz --output environment/app.tar.gz $(branch)

push: build
	docker login
	DOCKER_USER=$(docker info | grep "Username" | awk -F: '{print $NF}')
	docker tag eureka-api:latest ${DOCKER_USER}$(docker_io_image)
	docker push ${DOCKER_USER}$(docker_io_image)

shell:
	docker run --rm -it -v $(shell pwd):/src -p 18080:8080 eureka-api:latest bash

debug:
	docker run --rm -it -v $(shell pwd):/src -p 18080:8080 eureka-api:latest uvicorn app.main:app --reload --port 8080 --host 0.0.0.0 --log-level critical

run:
	docker run --rm -it -p 18080:8080 eureka-api:latest

test:
	docker run --rm -it -v $(shell pwd):/src eureka-api:latest python3 -m pytest --cov=app/ \
		--cov-report html --cov-report term --html=report/report.html \
		-v --self-contained-html $(tests)

test-in-docker:
	docker run -u root --rm -it eureka-api:latest python3 -m pytest --cov=app/ \
		--cov-report term  \
		-v --self-contained-html $(tests)

clean:
	docker rmi eureka-api:latest || true
	docker login
	DOCKER_USER=$(docker info | grep "Username" | awk -F: '{print $NF}')
	docker rmi ${DOCKER_USER}$(docker_io_image) || true
	rm -f environment/app.* || true
	rm -rf report htmlcov || true
