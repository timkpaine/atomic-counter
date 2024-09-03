PYTHON=python

.DEFAULT_GOAL := help
.PHONY: build build-sdist dev setup develop lint fix format tests test coverage checks check clean dist publish help

UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
	_CP_COMMAND := cp target/debug/libatomic_counter.dylib atomic_counter/atomic_counter.abi3.so
else
	_CP_COMMAND := cp target/debug/libatomic_counter.so atomic_counter/atomic_counter.abi3.so
endif

setup:  ## setup dev dependencies
	rustup component add rustfmt
	rustup component add clippy
	# cargo install cargo2junit
	# cargo install grcov
	python -m pip install maturin

develop:  ## build the library for development
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
	python -m pytest -v atomic_counter/tests --junitxml=junit.xml
	# cargo test -- --show-output
test: tests

coverage: $(eval SHELL:=/bin/bash)
	{ \
		# export CARGO_INCREMENTAL=0;\
		# export RUSTDOCFLAGS="-Cpanic=abort";\
		# export RUSTFLAGS="-Zprofile -Ccodegen-units=1 -Copt-level=0 -Clink-dead-code -Coverflow-checks=off -Zpanic_abort_tests -Cpanic=abort";\
		# cargo test -- -Z unstable-options --format json | cargo2junit > junit.xml;\
		# grcov . --llvm -s . -t lcov --branch --ignore-not-existing -o ./coverage.info;\
		python -m pytest -v atomic_counter/tests --junitxml=junit.xml --cov=atomic_counter --cov-branch --cov-fail-under=80 --cov-report term-missing --cov-report xml;\
	}

checks:  ## run checks
	cargo check --all-features
	python -m check_manifest
check: checks


clean:  ## clean the project
	git clean -fdx

dist: clean build build-sdist  ## create dists
	python -m twine check target/wheels/*

publish: dist  ## dist to pypi
	python -m twine upload target/wheels/* --skip-existing

# Thanks to Francoise at marmelab.com for this
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'
