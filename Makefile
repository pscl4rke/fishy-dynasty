
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

usage:
	@echo "Usage:"
	@sed -ne 's/^/| /;/@sed/!s/## //p' $(MAKEFILE_LIST) | (column -tl3 || cat)

venv: requirements.txt
	python3 -m venv $@
	$@/bin/pip install -r $^
	touch $@

webapp: ## Run the webserver in debug mode
webapp: export QUART_DEBUG := true
webapp: export QUART_SEND_FILE_MAX_AGE_DEFAULT := 1
webapp: | venv
	./venv/bin/python webapp.py
