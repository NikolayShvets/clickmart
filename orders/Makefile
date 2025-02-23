.POSIX:
.PHONY: all_checks clean env lint format typecheck test migrations migrate downgrade help
.DEFAULT_GOAL := help

# Переменные
UV := uv
RUFF_FLAGS := --fix

# Цвета для help
BLUE := \033[36m
NC := \033[0m

## Основные команды
all_checks: format lint typecheck test clean  ## Запустить все проверки

clean:  ## Очистить временные файлы и кэши
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

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

## Команды для разработки
lint:  ## Проверить код с помощью ruff
	$(UV) run ruff check $(RUFF_FLAGS) .

format:  ## Отформатировать код с помощью ruff
	$(UV) run ruff format .

typecheck:  ## Проверить типы с помощью mypy
	$(UV) run mypy .

test:  ## Запустить тесты с помощью pytest
	$(UV) run pytest .

migrations:  ## Создать новые миграции. Пример: make migrations m="initial_migration"
	$(UV) run alembic revision --autogenerate -m $(m)

migrate:  ## Применить миграции
	$(UV) run alembic upgrade head

downgrade:  ## Откатить миграции. Пример: make downgrade c=5f192388fca5; make downgrade c=-1
	$(UV) run alembic downgrade $(c)

## Вспомогательные команды
help:  ## Помощь по командам
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; \
		{printf "  $(BLUE)%-15s$(NC) %s\n", $$1, $$2}' 