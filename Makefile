.PHONY: challenges

help:
	@echo "available commands"
	@echo " - help               : information about available commands"
	@echo " - setup              : install Python virtual environments"
	@echo " - run                : run all challenges"

setup:
	@echo "Setting python version"
	pyenv local 3.9.6
	@echo "Creating virtual environment"
	pyenv exec python3 -m venv .env
	@echo "Installing Python packages"
	pip install -r requirements.txt

CHALLENGE_DIR = ./challenges

run:
	source .env/bin/activate && \
	$(foreach file, $(wildcard $(CHALLENGE_DIR)/*), echo $(file) && python3 $(file) && echo '---------';)
