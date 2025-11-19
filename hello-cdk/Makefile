SHELL := /usr/bin/env bash

PIP ?= pip3

PYTHON_VERSION := 3.13
ARTIFACT_VERSION ?= ""

.PHONY: checkOSDependencies
checkOSDependencies:
		@python3 --version | grep -q '${PYTHON_VERSION}' || (echo "Error: Python ${PYTHON_VERSION} is required" && exit 1)

.PHONY: venv
venv: checkOSDependencies
		python3 -m venv .venv

.PHONY: install
install: checkOSDependencies
		${PIP} install --upgrade pip
		${PIP} install -r requirements.txt
		${PIP} install -r requirements-dev.txt
		npm --prefix ../ install

.PHONY: lint
lint:
		pylint --recursive=y .

package:
		rm -f lambda-${ARTIFACT_VERSION}.zip
		pushd hello_cdk/lambda_src && \
		zip -9r lambda-${ARTIFACT_VERSION}.zip ./ -x "*.venv*" "tests/*" requirements*.txt "*/__pycache__/*" "*__pycache__*" && \
		mv lambda-${ARTIFACT_VERSION}.zip ../../ && \
		popd

.PHONY: synth
synth: package
		npx aws-cdk synth

.PHONY: scan
scan:
		checkov --config-file ../.checkov.yml -d ./cdk.out

.PHONY: diff
diff:
		npx aws-cdk diff

.PHONY: deploy
deploy:
		npx aws-cdk deploy --all

.PHONY: clean
clean:
		$(info Destroying environment ...)
		rm -rf ./.venv ./cdk.out lambda-*.zip
