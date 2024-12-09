PYTHON=python

.DEFAULT_GOAL := help
.PHONY: build build-sdist dev develop lint fix format tests test coverage checks check clean dist publish help

UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
	_CP_COMMAND := cp target/debug/libatomic_counter.dylib atomic_counter/atomic_counter.abi3.so
else
	_CP_COMMAND := cp target/debug/libatomic_counter.so atomic_counter/atomic_counter.abi3.so
endif

develop:  ## build the library for development
	rustup component add rustfmt
	rustup component add clippy
	cargo install cargo-nextest 
	cargo install cargo-llvm-cov
	python -m pip install -e .[develop]

build:  ## build the library
	maturin build

build-sdist:  ## build the sdist
	maturin sdist

dev: build  ## lightweight in-place build
	$(_CP_COMMAND)

lint:  ## run linters
	cargo clippy --all-features
	cargo fmt --all -- --check
	python -m ruff check atomic_counter
	python -m ruff format --check atomic_counter

fix:  ## run autofixers
	cargo fmt --all
	python -m ruff format atomic_counter
	python -m ruff check --fix atomic_counter

format: fix

tests:  ## run tests
	python -m pytest -v atomic_counter/tests

test: tests

coverage:
	python -m pytest -v atomic_counter/tests --cov=atomic_counter --cov-report term-missing --cov-report xml

checks:  ## run checks
	cargo check --all-features
	python -m check_manifest
check: checks


clean:  ## clean the project
	git clean -fdx

.PHONY: dist-py-wheel dist-py-sdist dist-rust dist-check dist publish

dist-py-wheel:  # build python wheel
	python -m cibuildwheel --output-dir dist

dist-py-sdist:  # build python sdist
	python -m build --sdist -o dist

dist-rust:  # build rust dists
	make -C rust dist

dist-check:  ## run python dist checker with twine
	python -m twine check dist/*

dist: clean build dist-rust dist-py-wheel dist-py-sdist dist-check  ## build all dists

publish: dist  # publish python assets

# Thanks to Francoise at marmelab.com for this
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'
