.PHONY: build test

build:
	docker build -t flood-pipeline .

test:
	docker run --rm flood-pipeline