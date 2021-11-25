build: environment/Dockerfile environment/requirements.txt
	docker rmi eureka-api:latest
	docker build -f environment/Dockerfile \
	--build-arg USERNAME=${USER} \
	--build-arg UID=$(shell id -u) \
	--build-arg GID=$(shell id -g) \
	-t eureka-api environment/

test:
	docker run --rm -it -v $(shell pwd):/src eureka-api:latest \
		python3 -m pytest --cov=src/ --cov-report html --cov-report term --html=report/report.html \
		-v --self-contained-html tests/

shell:
	docker run --rm -it -v $(shell pwd):/src -p 18080:8080 eureka-api:latest bash

debug:
	docker run --rm -it -v $(shell pwd):/src -p 18080:8080 eureka-api:latest uvicorn app.main:app --reload --port 8080 --host 0.0.0.0

clean:
	docker rmi eureka-api:latest
	rm -rf report
