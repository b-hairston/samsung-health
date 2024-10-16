# Project Name
PROJECT_NAME = samsung-health

# Conda environment name
ENV_NAME = samsung-health

# Directories to create
DIRS = $(PROJECT_NAME) tests

# Files to create
FILES = $(PROJECT_NAME)/__init__.py \
        $(PROJECT_NAME)/main.py \
        tests/test_main.py \
        .gitignore \
        README.md \
        environment.yml \
        setup.py \
        pyproject.toml

# Default target: create project structure and Conda environment
all: init create_conda_env

# Target to create directories and files
init:
	@echo "Creating project structure..."
	@mkdir -p $(DIRS)
	@touch $(FILES)
	@echo "__pycache__/" > .gitignore
	@echo "# $(PROJECT_NAME)" > README.md
	@echo "name: $(ENV_NAME)" > environment.yml
	@echo "dependencies:" >> environment.yml
	@echo "  - python=3.10" >> environment.yml
	@echo "Project structure created!"

# Target to create Conda environment from environment.yml
create_conda_env:
	@echo "Creating Conda environment: $(ENV_NAME)..."
	conda env create -f environment.yml || echo "Environment already exists!"
	@echo "Conda environment created!"

# Clean the project structure (delete directories, files, and Conda environment)
clean:
	@echo "Cleaning project structure and Conda environment..."
	@rm -rf $(DIRS)
	@rm -f $(FILES)
	@rm -f .gitignore README.md setup.py environment.yml pyproject.toml
	conda remove --name $(ENV_NAME) --all -y || echo "Environment does not exist!"
	@echo "Cleaned!"

# Install dependencies using Conda (update environment)
install:
	@echo "Installing dependencies..."
	conda env update -f environment.yml

# Run tests using pytest
test:
	@echo "Running tests..."
	conda run -n $(ENV_NAME) pytest

# Activate Conda environment (for manual usage)
activate:
	@echo "To activate the Conda environment, run:"
	@echo "    conda activate $(ENV_NAME)"

# Help
help:
	@echo "Available targets:"
	@echo "  all      - Create project structure and Conda environment"
	@echo "  clean    - Remove project structure and Conda environment"
	@echo "  install  - Install or update dependencies"
	@echo "  test     - Run tests with pytest in Conda environment"
	@echo "  activate - Instructions to activate the Conda environment"
