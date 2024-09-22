VENV_NAME := venv
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip
UVICORN := $(VENV_NAME)/bin/uvicorn
CURL := curl

include .env
export $(shell sed 's/=.*//' .env)

.PHONY: setup install run api clean

setup: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
	python3 -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt

install: setup
	$(PIP) install -r requirements.txt

run: setup
	$(UVICORN) main:app --reload

api: setup
	$(CURL) -X POST "http://localhost:8000/scrape" \
		-H "Content-Type: application/json" \
		-H "token: $(STATIC_TOKEN)" \
		-d '{"page_limit": $(PAGE_LIMIT)}'

clean:
	rm -rf $(VENV_NAME)
	rm -rf images
	rm -rf data.json
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

all: setup