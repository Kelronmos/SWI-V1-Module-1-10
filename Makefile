.PHONY: help setup extract install test clean logs dev format lint type docs

# Default target
.DEFAULT_GOAL := help

help: ## Display this help message
	@echo "SWI V1 Module 1-10 - Make Commands"
	@echo "==================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

extract: ## Extract swi_v1_part1_source.zip
	@echo "Extracting source ZIP..."
	python3 extract_and_setup.py

install: ## Install dependencies
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt

setup: extract install ## Full setup (extract + install)
	@echo "✅ Setup complete!"
	@echo "Next: source swi_env/bin/activate && make test"

test: ## Run all tests with coverage
	@echo "Running tests..."
	cd swi_v1_part1_source && python3 -m pytest tests/test_swi_core.py -v --cov=src --cov-report=term-color

test-unit: ## Run unit tests only
	@echo "Running unit tests..."
	cd swi_v1_part1_source && python3 -m pytest tests/test_swi_core.py -v -m unit

test-integration: ## Run integration tests
	@echo "Running integration tests..."
	cd swi_v1_part1_source && python3 -m pytest tests/test_swi_core.py -v -m integration

test-coverage: ## Generate HTML coverage report
	@echo "Generating coverage report..."
	cd swi_v1_part1_source && python3 -m pytest tests/ --cov=src --cov-report=html --cov-report=term-color
	@echo "Report: open htmlcov/index.html"

clean: ## Remove build artifacts and cache
	@echo "Cleaning..."
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	@echo "✅ Clean complete"

clean-all: clean ## Remove all temporary files including logs
	@echo "Cleaning all temporary files..."
	rm -rf .swi_temp logs/*.jsonl
	@echo "✅ Full clean complete"

logs: ## Show recent logs
	@tail -50 logs/audit.jsonl 2>/dev/null || echo "No logs yet. Run 'make test' first."

logs-watch: ## Watch logs in real-time
	@tail -f logs/audit.jsonl 2>/dev/null || echo "No logs yet"

dev: ## Setup development environment
	@echo "Setting up development environment..."
	pip install -r requirements.txt
	pip install black flake8 mypy
	@echo "✅ Development setup complete"

format: ## Format code with black
	@echo "Formatting code..."
	black swi_v1_part1_source/src swi_v1_part1_source/tests
	@echo "✅ Formatting complete"

lint: ## Run linter
	@echo "Running linter..."
	flake8 swi_v1_part1_source/src swi_v1_part1_source/tests --max-line-length=100
	@echo "✅ Linting complete"

type: ## Run type checker
	@echo "Running type checker..."
	mypy swi_v1_part1_source/src
	@echo "✅ Type checking complete"

quality: format lint type ## Run all quality checks
	@echo "✅ Quality checks complete"

docs: ## Generate documentation
	@echo "Documentation files:"
	@ls -lh README.md SETUP_GUIDE.md INSTALLATION.md

venv: ## Create virtual environment
	@echo "Creating virtual environment..."
	python3 -m venv swi_env
	@echo "Activate with: source swi_env/bin/activate"

envfile: ## Create .env from template
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env from template"; \
		echo "Edit .env to customize configuration"; \
	 else \
		echo ".env already exists"; \
	 fi

status: ## Show installation status
	@echo "Installation Status"
	@echo "==================="
	@echo "Python: $$(python3 --version)"
	@echo "Pytest: $$(python3 -m pytest --version 2>/dev/null || echo 'Not installed')"
	@echo "Config file: $$([ -f config/swi_config.yaml ] && echo '✅' || echo '❌')"
	@echo "Virtual env: $$([ -d swi_env ] && echo '✅' || echo '❌')"
	@echo "Source extracted: $$([ -d swi_v1_part1_source ] && echo '✅' || echo '❌')"

info: ## Display system information
	@echo "System Information"
	@echo "=================="
	@echo "OS: $$(uname -s)"
	@echo "Python: $$(python3 --version)"
	@echo "Pip: $$(pip --version)"
	@echo "Git: $$(git --version 2>/dev/null || echo 'Not installed')"

.PHONY: $(MAKEFILE_LIST)
