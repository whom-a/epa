# Event Posting App (EPA)

[![Last Commit](https://img.shields.io/github/last-commit/NateMartes/epa)](https://github.com/NateMartes/epa/commits)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
[![AWS](https://custom-icon-badges.demolab.com/badge/AWS-%23FF9900.svg?logo=aws&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](#)
[![Go](https://img.shields.io/badge/Go-%2300ADD8.svg?&logo=go&logoColor=white)](#)
[![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?logo=mongodb&logoColor=white)](#)
[![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?logo=redis&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)

Safety is important and as technology gets more sophisticated, so should our ability to stay safe. Our project EPA, the Event Posting App, will be a mobile application that allows users to post about safety concerns in local areas to ensure that users know what is going on in their community. Users can subscribe to categories and specific tags within those categories and be notified as soon as an event occurs.

## System Architecture

The overview of EPA can appear as such:

![EPA System Architecture](./system_diagram/event-posting-app.png "EPA System Architecture")

---
## The EPA API

The EPA API uses a Contract-First approach, meaning endpoints are auto generated from an OpenAPI spec using the `openapi-generator-cli` tool:

Installing the tool uses `npm`:
```bash
npm install -g @openapitools/openapi-generator-cli
```

Then you can generate the API endpoints like such:
```bash
openapi-generator-cli generate \
-i openapi.yaml \
-g python-fastapi \
-o . \ --additional-properties=packageName=epa_api,fastapiImplementationPackage=api_implementation
```

The service methods (the actual logic of the API) is stored within the `./api/src/epa_api/api_implementation` directory.

### Adding Endpoints
When adding endpoints, update the `openapi.yml` file with the new endpoint information and run the previous command. Then add the new method to the `./api/src/epa_api/api_implementation/` directory. The function that the API will call **MUST** be defined by the `operationId`

Example:
```yaml
paths:
  /status:
    get:
      operationId: get_status # HERE: function should be called `get_status`
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Status"
          description: API is healthy
      summary: Check API health
```

Then you can add the code in the `./api/src/epa_api/api_implementation/` directory:
```python
from epa_api.apis.default_api_base import BaseDefaultApi
from epa_api.models.status import Status

class EpaAPIImplementation(BaseDefaultApi):
    async def get_status(self) -> Status:
        return Status(status="healthy", version="1.0.0")
```

---
## The Database
The database uses MongoDB to store a `users` collection and `posts` collection.
The database is initialized using a Python script and the `config.json` file found within the `./database` directory.
You can spin up the database using `docker compose`. The initializer will add the needed collections from the `config.json` file.

---
## User Timeline Caching
To ensure a user can see a post very quickly, we preform caching on post and store them into a Redis database.
The provider for this service is Upstash. You can locally test this database using the `docker-compose.yml` file in the
`./user_timeline_post_cache` directory to simulate Upstash.

---
## The Post Queue

---
## The Notifier

---
## The Post Ingestor

___
## The User Cache Loader

---
## The EPA Moblie App

---
## Useful Commands

Set environment variables from `.env`:
```bash
export $(grep -v '^#' .env | xargs)
```

Unset environment variables from `.env`:
```bash
unset $(grep -v '^#' .env | sed -E 's/(.*)=.*/\1/' | xargs)
```
