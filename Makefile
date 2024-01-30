SHELL := /bin/bash

VENV_PATH = venv/bin/activate

venv:
	@echo "Creating virtual environment..."
	python3 -m venv venv

install:
	@echo "Checking virtual environment..."
	[ -f "$(VENV_PATH)" ] || $(MAKE) venv
	@echo "Installing requirements..."
	. $(VENV_PATH) && pip install -r requirements.txt && deactivate

makemigrations:
	. $(VENV_PATH) && python manage.py makemigrations && deactivate

migrate:
	. $(VENV_PATH) && python manage.py migrate && deactivate

pre-commit-setup:
	@echo "Running pre-commit checks on all files..."
	brew install pre-commit
	pre-commit run --all-files

run-server: install makemigrations migrate
	@echo "Running development server..."
	. $(VENV_PATH) && python manage.py runserver 8002
