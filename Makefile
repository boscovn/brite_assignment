clean: clean_dev clean_test
clean_dev:
	OMDB_API_KEY=IGNORE docker compose down --volumes
	OMDB_API_KEY=IGNORE docker compose rm -f
clean_test:
	docker compose -f test.compose.yaml down --volumes
	docker compose -f test.compose.yaml rm -f
test_unit:
	docker build -t movies-api-test --target test ./movies-api
	docker run --rm movies-api-test

setup_e2e_env: clean_test
	docker compose -f test.compose.yaml up --build -d --scale e2e=0
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
	make clean_dev

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
	make clean_test

