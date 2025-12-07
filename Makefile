.PHONY: help install install-dev lint format check fix clean run test

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

lint: ## Run linter
	ruff check .

format: ## Format code
	ruff format .

check: ## Check linting and formatting (no fixes)
	ruff check .
	ruff format --check .

fix: ## Auto-fix linting and format code
	ruff check --fix .
	ruff format .

clean: ## Clean up cache files
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

run: ## Run the development server
	python run.py

test: ## Run tests (if available)
	@echo "No tests configured yet"
