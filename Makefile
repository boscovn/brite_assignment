clean:
	docker compose down
	docker compose rm -f
	docker compose -f test.compose.yaml down
	docker compose -f test.compose.yaml rm -f
	#
test_unit:
	docker build -t movies-api-test --target test ./movies-api
	docker run --rm movies-api-test

test_e2e: clean
	docker compose -f test.compose.yml up --build --abort-on-container-exit

test: clean
	@echo "Running unit tests"
	make test_unit
	@echo "Running end-to-end tests"

