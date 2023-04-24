launch: ## Launch the new text
	./launch.sh

####----Basic configurations----####
.PHONY: pre-commit
install_pre_commit: ## configure and install pre commit tool
	@poetry run pre-commit install

uninstall_pre_commit: ## configure and install pre commit tool
	@poetry run pre-commit uninstall

.PHONY: install
install: ## Install the poetry and python environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@poetry shell

.PHONY: check_project
check_project: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry lock --check
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a

	# This is different from the gitleaks pre-commit since it checks also unstaged files
	@gitleaks protect --no-banner --verbose
# echo "🚀 Checking for obsolete dependencies: Running deptry"
# poetry run deptry .

.PHONE: poetry_plugins
poetry_plugins_install: ## Install and configure the poetry plugins
	@echo "Install poetry-plugin-sort"
	@poetry self add poetry-plugin-sort

poetry_plugins: ## Launch the poetry plugins
	@echo "Launching poetry-plugin-sort"
	@poetry sort

####----Docker----####
logout: ## Logout to docker private registry
	@docker logout

launch_docker: ## Launch the docker compose and containers
	@docker-compose -p template up --build -d

build: ## Build the docker compose and containers
	@docker-compose -p template build

launch_prod: ## Launch the launch.sh file as in production mode
	@./launch.sh

check: ## Check the logs for the docker containers
	@docker ps -a | grep "template"

stop: ## Stop the docker containers
	@docker-compose -p template down

stop_clear: ## Stop the docker containers and clean the volumes
	@docker-compose -p template down -v

clean_volumes: ## Clean the volumes
	@docker volume prune

####----Project----####
.PHONY: poetry_build
package_build: # Build the package
	@poetry build

.PHONY: publish_pypi
pypi: # publish in the public pypy registry
	@python setup.py sdist
	@python setup.py bdist_wheel --universal
	@twine upload dist/*

### Project specific tasks
.PHONY: project
launch_py3: # Launch the main file with python 3
	@export PYTHONPATH=$(pwd) && python3 app/main.py

.PHONY: project
launch_py: # Launch the main file with python
	@export PYTHONPATH=$(pwd) && python app/main.py

.PHONY: help
help: ## Ask for help in the Makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

#### Project clean
.PHONY: project_clean
clean: ## Clean the projects of unwanted cached folders
	@rm -rf **/.ipynb_checkpoints **/.pytest_cache **/__pycache__ **/**/__pycache__ ./notebooks/ipynb_checkpoints .pytest_cache ./dist ./volumes

.PHONY: project_restore
restore: ## Restore the projects to the start (hard clean)
	@rm -rf **/.ipynb_checkpoints **/.pytest_cache **/__pycache__ **/**/__pycache__ ./notabooks/ipynb_checkpoints .pytest_cache ./dist .venv poetry.lock

.secrets_baseline.json:  ## Create secrets baseline
	gitleaks detect --redact --report-path "$@" || true

.DEFAULT_GOAL := help