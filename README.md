# Challenge ERKLABs

## Description

Challenge API proxy to enhancement its behave

## Requeriments

- [Link to the description](https://github.com/eurekalabs-io/challenges/blob/main/backend/python/stock-market-service.md)

## Usage and Options

To run the test sute you need build the local dev environment and the run the test, to build the environment in the script directory you have to run ***make build*** and to execute the test suite ***make run***

```bash
make build
# Build the docker environment, it will create the docker with non-root user

make push
# This command will try to push docker images to docker.io, it will run docker login to try to log in in to docker.io using the local credentials. For instance, it will try to push docker.io/<username>/eureka-api:latest

make test
# Run tests, its output will be generated in report/ and htmlcov/ directories

make test-in-docker
# Run tests, using the test files contained in docker image


make shell
# Attach to docker instance

make run
# Run docker image using CMD configuration in Dockerfile

make debug
# Run docker image using sharing the code between the host and the container, this command should be used to develop.

make clean
#Clean remove docker image and report generate by tests
```

## Directories and files

- app/ contains python files.
- tests/ contains test scripts.
- terraform/ IaaC files to deploy the API in AWS ECS Service.
- report contains pytest report after running tests.
- htmlcov contains test coverage.

## Flake8 rules

My IDE is using flake8 for style guide enforcement and this is the current configuration.
So, it could have some diference with PEP8 Style Guide, for instance, max-line-length.

```
[flake8]
ignore = E203, E266, W503, W605, E111
max-line-length = 100
exclude=.
    venv
    .git
    .tox
select = B,C,E,F,W,T4,B9
```

## API Endpoints

Once you run it using ***make run*** or ***make debug***, you should go to http://localhost:18080/docs to get API documentation.
(API listen in 8080 but docker map it to 18080)
Endpoints:

- ***/health_check:*** This endpoint is needed for AWS Load balnacer to keep the docker instances alive.
- ***/auth:*** Contains the endpoints necessary to sign up/sign in the users
- ***/stocks:*** Use this endpoint to get a list of companies allowed to make queries, for instance, Facebook, Amazon, Google, etc.
- ***/stocks/{company_id}:*** Use this endpoint to get a stock market data from a company.

'''

## Improvements

- Integrate an external database to persist the users.
- Horinzontal scaling will be supported if external database is implemented.
- Implements Token Bucket algorithm for throttling, right now it implement a Generic Cell Rate Algorithm to allow a constant request rate, for instance, 4 request per second.
- By default when user signup it will be enabled, a good practice would be to send an email with a link to validate the user and activate it. Using services line SNS or SES from AWS or SendInBlue we can solve it, but I consider it out of scope for this code challenge.

'''

---
Author:

- Francisco Giana <gianafrancisco@gmail.com>

---
