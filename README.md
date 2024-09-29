# Secret Santa API

This is a RESTful API built with FastAPI and SQLModel for managing participants in a Secret Santa event with multiple lists and blacklist functionality.

## Setup

### 1. Install dependencies

Make sure you have **Poetry** installed. Then, run the following command to install all dependencies:

```bash
poetry install
```

### 2. Run the application locally

To start the FastAPI application, use the following command:

```bash
poetry run uvicorn app.main:app --reload
```

This will start the API on [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

### 1. POST /participants

This endpoint allows you to create a new participant in the default Secret Santa list.

**Example:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/participants' \
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
  "name": "John Doe"
}
```

### 2. GET /participants

This endpoint retrieves a list of all participants currently registered in the default Secret Santa list.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/participants' \
  -H 'accept: application/json'
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "John Doe"
  },
  {
    "id": 2,
    "name": "Jane Smith"
  }
]
```

### 3. POST /blacklist

This endpoint allows one participant to blacklist another participant in the default list, preventing them from being paired together in the Secret Santa draw.

**Example:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/blacklist' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"participant_id": 1, "blacklisted_participant_id": 2}'
```

**Request Body:**

```json
{
  "participant_id": 1,
  "blacklisted_participant_id": 2
}
```

**Response:**

```json
{
  "id": 1,
  "participant_id": 1,
  "blacklisted_participant_id": 2
}
```

### 4. GET /draw

This endpoint generates a valid Secret Santa draw for the default list, ensuring that no participants are paired with someone on their blacklist.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/draw' \
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

### 5. POST /lists

Create a new Secret Santa list. If no name is provided, one will be generated automatically using a Star Wars planet name.

**Example:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/lists' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Holiday 2024"}'
```

**Response:**

```json
{
  "id": 1,
  "name": "Holiday 2024"
}
```

### 6. POST /lists/{list_id}/participants

Add a new participant to a specific Secret Santa list.

**Example:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/lists/1/participants' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name":"John Doe"}'
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe",
  "list_id": 1
}
```

### 7. GET /lists/{list_id}/participants

Retrieve all participants for a specific Secret Santa list.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/lists/1/participants' \
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

### 8. GET /lists/{list_id}/draw

Generate a Secret Santa draw for a specific list.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/lists/1/draw' \
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

### 9. DELETE /participants/{participant_id}

Delete a participant from the default Secret Santa list.

**Example:**

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/participants/1' \
  -H 'accept: application/json'
```

**Response:**

```json
{
  "message": "Participant John Doe (id: 1) removed from default list"
}
```

### 10. DELETE /lists/{list_id}/participants/{participant_id}

Delete a participant from a specific Secret Santa list.

**Example:**

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/lists/1/participants/1' \
  -H 'accept: application/json'
```

**Response:**

```json
{
  "message": "Participant John Doe (id: 1) removed from list with id: 1"
}
```

### 11. DELETE /lists/{list_id}

Delete a specific Secret Santa list along with all its participants.

**Example:**

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/lists/1' \
  -H 'accept: application/json'
```

**Response:**

```json
{
  "message": "List with id: 1 and all associated participants have been removed"
}
```

### 12. GET /lists/with-participants

Retrieve all Secret Santa lists with their participants.

**Example:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/lists/with-participants' \
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

- **POST /participants**: Add a new participant.
- **GET /participants**: Get a list of all participants.
- **POST /blacklist**: Add a participant to another participant's blacklist.
- **GET /draw**: Generate a valid Secret Santa draw, respecting blacklists.
- **POST /lists**: Create a new Secret Santa list.
- **POST /lists/{list_id}/participants**: Add a participant to a specific list.
- **GET /lists/{list_id}/participants**: Retrieve all participants in a list.
- **GET /lists/{list_id}/draw**: Generate a Secret Santa draw for a specific list.
- **DELETE /participants/{participant_id}**: Delete a participant from the default list.
- **DELETE /lists/{list_id}/participants/{participant_id}**: Delete a participant from a specific list.
- **DELETE /lists/{list_id}**: Delete a specific list with all its participants.
- **GET /lists/with-participants**: Get all lists with their participants.

## Important Resources

Here are some helpful links and resources related to the project:

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
