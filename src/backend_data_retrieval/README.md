# Path of Modifiers Backend Data Retrieval documentation

## Development

### Requirements

- [Docker Engine or Docker Desktop](https://docs.docker.com/engine/install/)
- [uv for Python package manager](https://docs.astral.sh/uv/)

### Docker compose

Check out the guide in [../development.md](https://github.com/Path-of-Modifiers/pathofmodifiersapp/blob/main/development.md)

### uv

Install dependencies and activate environment with:

```bash
cd backend_data_retrieval

uv sync

source .venv/bin/activate
```


### How to run tests

#### Test prerequisites

You need to build `Dockerfile.test` within module `backend_data_retrieval`.

To build the container, run:

```bash
docker build -t backend_data_retrieval_test -f backend_data_retrieval/Dockerfile.test backend_data_retrieval
```

#### Run tests

To run all tests, run this command:

```bash
docker run --rm backend_data_retrieval_test
```

If you want to specify a test file, run it like this for example:

```bash
docker run --rm backend_data_retrieval_test data_retrieval_app/tests/external_data_retrieval/test_continuous_data_retrieval.py
```
