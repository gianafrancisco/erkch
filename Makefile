docker_io_image = "fgiana/eureka-api:latest"
branch = "main"

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
	docker tag eureka-api:latest $(docker_io_image)
	docker push $(docker_io_image)

test:
	docker run --rm -it -v $(shell pwd):/src eureka-api:latest \
		python3 -m pytest --cov=src/ --cov-report html --cov-report term --html=report/report.html \
		-v --self-contained-html tests/

shell:
	docker run --rm -it -v $(shell pwd):/src -p 18080:8080 eureka-api:latest bash

debug:
	docker run --rm -it -v $(shell pwd):/src -p 18080:8080 eureka-api:latest uvicorn app.main:app --reload --port 8080 --host 0.0.0.0

run:
	docker run --rm -it -p 18080:8080 eureka-api:latest

clean:
	docker rmi eureka-api:latest
	docker rmi $(docker_io_image)
	rm -f environment/app.*
