# Secret Santa API

This is a RESTful API built with FastAPI and SQLModel for managing participants in a Secret Santa event with multiple lists and blacklist functionality.

## Setup

### 1. Install Dependencies

Make sure you have **Poetry** installed. Then, run the following command to install all dependencies:

```bash
poetry install
```

### 2. Run the Application Locally

To start the FastAPI application, use the following command:

```bash
poetry run uvicorn app.main:app --reload
```

This will start the API on [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

### 1. **POST /v1/participants**

This endpoint allows you to create a new participant in the default Secret Santa list.

**Example:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/v1/participants/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name":"John Doe"}'
```

**Request Body:**

```json
{
  "name": "John Doe"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe",
  "list_id": 1,
}
```

### 2. **GET /v1/participants**

This endpoint retrieves a list of all participants currently registered in the default Secret Santa list.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/participants/' \
  -H 'accept: application/json'
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "list_id": 1,
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "list_id": 1,
  }
]
```

### 3. **POST /v1/blacklist**

This endpoint allows one participant to blacklist another participant in the default list, preventing them from being paired together in the Secret Santa draw.

**Example:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/v1/blacklist/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"participant_id": 1, "blacklisted_participant_id": 2}'
```



**Response:**

```json
{
  "id": 1,
  "participant_id": 1,
  "blacklisted_participant_id": 2,
  "list_id": 1,
}
```

### 4. **GET /v1/draw**

This endpoint generates a valid Secret Santa draw for the default list, ensuring that no participants are paired with someone on their blacklist.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/draw/' \
  -H 'accept: application/json'
```

**Response:**

```json
[
  {
    "gifter_id": 1,
    "gifter_name": "John Doe",
    "receiver_id": 2,
    "receiver_name": "Jane Smith"
  },
  {
    "gifter_id": 2,
    "gifter_name": "Jane Smith",
    "receiver_id": 1,
    "receiver_name": "John Doe"
  }
]
```

### 5. **POST /v1/lists**

Create a new Secret Santa list. One will be generated automatically using a Star Wars planet name.

**Example without name:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/v1/lists/' \
  -H 'accept: application/json'
```


### 6. **POST /v1/lists/{list_id}/participants**

Add a new participant to a specific Secret Santa list.

**Example:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/v1/lists/1/participants/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name":"John Doe"}'
```

**Request Body:**

```json
{
  "name": "John Doe"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe",
  "list_id": 1
}
```

### 7. **GET /v1/lists/{list_id}/participants**

Retrieve all participants for a specific Secret Santa list.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/lists/1/participants/' \
  -H 'accept: application/json'
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "list_id": 1
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "list_id": 1
  }
]
```

### 8. **GET /v1/lists/{list_id}/draw**

Generate a Secret Santa draw for a specific list.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/lists/1/draw/' \
  -H 'accept: application/json'
```

**Response:**

```json
[
  {
    "gifter_id": 1,
    "gifter_name": "John Doe",
    "receiver_id": 2,
    "receiver_name": "Jane Smith"
  },
  {
    "gifter_id": 2,
    "gifter_name": "Jane Smith",
    "receiver_id": 1,
    "receiver_name": "John Doe"
  }
]
```

### 9. **DELETE /v1/participants/{participant_id}**

Delete a participant from the default Secret Santa list.

**Example:**

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/v1/participants/1' \
  -H 'accept: application/json'
```

**Response:**

```json
{
  "message": "Participant John Doe (id: 1) removed from default list"
}
```

### 10. **DELETE /v1/lists/{list_id}/participants/{participant_id}**

Delete a participant from a specific Secret Santa list.

**Example:**

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/v1/lists/1/participants/1' \
  -H 'accept: application/json'
```

**Response:**

```json
{
  "message": "Participant John Doe (id: 1) removed from list with id: 1"
}
```

### 11. **DELETE /v1/lists/{list_id}**

Delete a specific Secret Santa list along with all its participants.

**Example:**

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/v1/lists/1' \
  -H 'accept: application/json'
```

**Response:**

```json
{
  "message": "List with id: 1 and all associated participants have been removed"
}
```

### 12. **GET /v1/lists/with-participants**

Retrieve all Secret Santa lists with their participants.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/v1/lists/with-participants' \
  -H 'accept: application/json'
```

**Response:**

```json
[
  {
    "list_id": 1,
    "list_name": "Holiday 2024",
    "participants": [
      {
        "id": 1,
        "name": "John Doe"
      },
      {
        "id": 2,
        "name": "Jane Smith"
      }
    ]
  },
  {
    "list_id": 2,
    "list_name": "Tatooine-123456",
    "participants": [
      {
        "id": 3,
        "name": "Alice"
      },
      {
        "id": 4,
        "name": "Bob"
      }
    ]
  }
]
```

## Running Tests

To run all unit tests for the API, execute the following command:

```bash
poetry run pytest
```

This will run all the tests to ensure the API's functionality is working as expected.

## Summary of Endpoints

- **POST /v1/participants**: Add a new participant to the default list.
- **GET /v1/participants**: Get a list of all participants in the default list.
- **POST /v1/blacklist**: Add a participant to another participant's blacklist in the default list.
- **GET /v1/draw**: Generate a valid Secret Santa draw for the default list, respecting blacklists.
- **POST /v1/lists**: Create a new Secret Santa list.
- **POST /v1/lists/{list_id}/participants**: Add a participant to a specific list.
- **GET /v1/lists/{list_id}/participants**: Retrieve all participants in a list.
- **GET /v1/lists/{list_id}/draw**: Generate a Secret Santa draw for a specific list.
- **DELETE /v1/participants/{participant_id}**: Delete a participant from the default list.
- **DELETE /v1/lists/{list_id}/participants/{participant_id}**: Delete a participant from a specific list.
- **DELETE /v1/lists/{list_id}**: Delete a specific list with all its participants.
- **GET /v1/lists/with-participants**: Get all lists with their participants.

## Important Resources

Here are some helpful links and resources related to the project:

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Poetry](https://python-poetry.org/docs/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pytest](https://docs.pytest.org/en/stable/)

