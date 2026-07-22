COMPOSE_FILE := compose.yaml
COMPOSE := docker compose -f $(COMPOSE_FILE)
SCRIPTS_DIR := scripts


.PHONY: up down logs

help:
	@echo '* targets: up - down - logs'

gen_compose:
	PYTHONPATH=$(SCRIPTS_DIR) uv run $(SCRIPTS_DIR)/gen_compose.py $(COMPOSE_FILE)

up: gen_compose
	$(COMPOSE) up --build --remove-orphans --detach

down: gen_compose
	$(COMPOSE) stop -t 5
	$(COMPOSE) down --volumes --remove-orphans

logs: gen_compose
	$(COMPOSE) logs -f
