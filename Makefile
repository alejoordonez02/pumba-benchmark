COMPOSE_FILE := compose.yaml
COMPOSE := docker compose -f $(COMPOSE_FILE)

.PHONY: up down logs

help:
	@echo '* targets: up - down - logs'

gen_compose:
	uv run gen_compose.py $(COMPOSE_FILE)

up: gen_compose
	mkdir -p responses
	$(COMPOSE) up --build --remove-orphans --detach

down: gen_compose
	$(COMPOSE) stop -t 5
	$(COMPOSE) down --volumes --remove-orphans

logs: gen_compose
	$(COMPOSE) logs -f $$SERVICES; \
