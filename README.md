# Brite Assignment

## Introduction

This project aims to meet the goals of the task defined [here](task.md).

## Overview

The repository contains the a directory for the API itself, a directory for mocking the omdb API, a Makefile with useful commands, and docker compose files for running the API and running the end-to-end tests.

## Requirements

Everything is dockerized, so the requirements are:
- docker
- docker compose
- make

## Running the API

To avoid putting credentials in the repository, the API requires an environment variable `OMDB_API_KEY`
You need to export it before running the API.

```bash
export OMDB_API_KEY=your_api_key
make run
```

## Running the tests

There are unit tests and end-to-end tests.
You can run them both with

```bash
make test
```

Or you can run them separately with

```bash
make test-unit
```

```bash
make test-e2e
```

## To deploy in GCP

In order to deploy in a GCP project:
- Create a new project
- Create a VPC network
- Create a cloudsql postgres instance in the VPC network
- Create a redis instance in the VPC network
- Create a cloud run service with the following:
    - Container image: Image name and tag for the API, recommended to use ci/cd to build and push the image to the desired registry
    - Envorment variables to specify the database, redis, mongodb, and omdb credentials as well as appropriate values for the other variables
    - The sensitive variables should be stored in the secret manager and referenced in the cloud run service
    - Public access should be enabled, since the API handles its own authentication
    - The service should be connected to the VPC network where the cloudsql instance is located
