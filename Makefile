.PHONY: release-dev release-patch release-minor release-major help dummy do-release docs pubdocs
.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

docs: ## generate Sphinx HTML documentation, including API docs
	mkdir -p docs
	rm -rf docsrc/_autosummary
	ls -A1 docs | xargs -I {} rm -rf docs/{}
	$(MAKE) -C docsrc clean html
	cp -a docsrc/_build/html/. docs

pubdocs: docs ## Publish the documentation to GitHub
	ghp-import -op docs
