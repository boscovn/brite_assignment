clean:
	OMDB_API_KEY=notneeded docker compose down -v
	OMDB_API_KEY=notneeded
	docker compose -f test.compose.yaml down -v
	docker compose -f test.compose.yaml rm -f
	#
test_unit:
	docker build -t movies-api-test --target test ./movies-api
	docker run --rm movies-api-test

test_env:
	docker compose up --build -d

setup_e2e_env:
	docker compose -f test.compose.yaml up --build -d
test_e2e: setup_e2e_env
	docker compose -f test.compose.yaml run --rm e2e


run: clean
	@echo ".........................."
	@echo ".........................."
	@echo "Starting the application"
	@echo ".........................."
	@echo ".........................."
	docker compose up --build -d
	@echo ".........................."
	@echo ".........................."
	@echo "Application is running"
	@echo ".........................."
	@echo ".........................."

test: clean
	@echo ".........................."
	@echo ".........................."
	@echo "Running unit tests"
	@echo ".........................."
	@echo ".........................."
	make test_unit
	@echo ".........................."
	@echo ".........................."
	@echo "Running end-to-end tests"
	@echo ".........................."
	@echo ".........................."
	make test_e2e

