PIP ?= pip3

PYTHON_VERSION := 3.13

.PHONY: checkOSDependencies
checkOSDependencies:
		@python3 --version | grep -q '${PYTHON_VERSION}' || (echo "Error: Python ${PYTHON_VERSION} is required" && exit 1)

.PHONY: install
install: checkOSDependencies
		python3 -m venv .venv
		. ./.venv/bin/activate && ${PIP} install --upgrade pip
		. ./.venv/bin/activate && ${PIP} install -r requirements.txt
		. ./.venv/bin/activate && ${PIP} install -r requirements-dev.txt
		npm --prefix ../ install

.PHONY: lint
lint:
		. ./.venv/bin/activate && pylint --recursive=y .

package:
		pushd hello_cdk/lambda_src && \
		zip -9r lambda.zip ./ -x "*.venv*" "tests/*" requirements*.txt "*/__pycache__/*" "*__pycache__*" "__init__.py" && \
		mv lambda.zip ../../ && \
		popd

.PHONY: diff
diff:
		. ./.venv/bin/activate && npx aws-cdk diff

.PHONY: deploy
deploy:
		. ./.venv/bin/activate && npx aws-cdk deploy --all

.PHONY: clean
clean:
		$(info Destroying environment ...)
		rm -rf ./.venv ./cdk.out
