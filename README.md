# Event Posting App (EPA)

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
-i swagger.yml \
-g python-fastapi \
-o ./api \ --additional-properties=packageName=epa_api,fastapiImplementationPackage=api_implementation
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