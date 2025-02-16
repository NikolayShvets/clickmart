.POSIX:
.PHONY: up local down help env
.DEFAULT_GOAL := help

# Цвета для help
BLUE := \033[36m
NC := \033[0m

## Основные команды
up:  ## Запустить все сервисы в production режиме
	docker compose up -d --build

local:  ## Запустить сервисы для локальной разработки
	docker compose -f local-docker-compose.yml up

down:  ## Остановить все сервисы и удалить volumes
	docker compose down -v

env:  ## Создать .env файл из .env.example
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			cp .env.example .env; \
			echo ".env файл создан из .env.example"; \
		else \
			echo ".env.example файл не найден"; \
			exit 1; \
		fi \
	else \
		echo ".env файл уже существует"; \
	fi

## Вспомогательные команды
help:  ## Показать это сообщение
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; \
		{printf "  $(BLUE)%-15s$(NC) %s\n", $$1, $$2}'