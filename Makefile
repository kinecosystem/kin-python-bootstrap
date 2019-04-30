# Used to build/push dockers

VERSION := $(shell cat bootstrap/src/init.py | grep VERSION | head -1 | cut -d "'" -f 2)
IMAGE := kinecosystem/python-bootstrap

all:
	make build && make push && make update-compose

build:
	cd bootstrap && \
	docker build -t ${IMAGE}:${VERSION} .

push:
	docker push ${IMAGE}:${VERSION}
	# Dont push latest, be explicit with versions

update-compose:
	sed s@${IMAGE}.*@${IMAGE}:${VERSION}@g -i docker-compose.yml

.PHONY: build push
