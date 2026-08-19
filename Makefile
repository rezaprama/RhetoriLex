PYTHON ?= python
DIST_DIR ?= dist
PLUGIN_ZIP ?= $(DIST_DIR)/rhetorilex-plugin.zip

.DEFAULT_GOAL := help

.PHONY: help validate build test skill-check restricted-check package verify-package determinism pages check release-check

help:
	@echo "RhetoriLex developer targets"
	@echo "  make validate        Validate canonical data"
	@echo "  make build           Build public data and package resources"
	@echo "  make test            Run unit tests"
	@echo "  make skill-check     Validate bundled Codex skill"
	@echo "  make package         Build deterministic plugin ZIP + SHA-256"
	@echo "  make determinism     Compare two exact data/plugin rebuilds"
	@echo "  make pages           Prepare docs/ with generated phrases.json"
	@echo "  make check           Run full local quality gate"

validate:
	$(PYTHON) scripts/validate_data.py

build:
	$(PYTHON) scripts/build_data.py

test:
	$(PYTHON) -m unittest discover -s tests -v

skill-check:
	$(PYTHON) .github/scripts/validate_skill.py skills/rhetorilex

restricted-check:
	$(PYTHON) .github/scripts/check_tracked_files.py

package:
	$(PYTHON) scripts/package_plugin.py --output $(PLUGIN_ZIP)

verify-package: package
	$(PYTHON) scripts/package_plugin.py --verify $(PLUGIN_ZIP)

determinism:
	$(PYTHON) .github/scripts/check_determinism.py

pages: build
	$(PYTHON) .github/scripts/prepare_pages.py

check: restricted-check validate build test skill-check verify-package determinism

release-check: check pages
