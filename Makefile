COMPOSE_FILE := docker-compose.yaml
COMPOSE := docker compose -f $(COMPOSE_FILE)

.PHONY: up down logs

help:
	@echo '* targets: up - down - logs'

up:
	mkdir -p responses
	$(COMPOSE) up --build --remove-orphans --detach
down:
	$(COMPOSE) stop -t 5
	$(COMPOSE) down --volumes --remove-orphans

logs:
	$(COMPOSE) logs -f $$SERVICES; \
