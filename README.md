# Secret Santa API

This is a RESTful API built with FastAPI and SQLModel for managing participants in a Secret Santa event with blacklist functionality.

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

This will start the API on `http://127.0.0.1:8000`.

---

## API Endpoints

### 1. `POST /participants`

This endpoint allows you to create a new participant.

#### Example:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/participants' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name":"John Doe"}'
```

#### Request Body:

```json
{
  "name": "John Doe"
}
```

- **`name`**: The name of the participant. Must be between 1 and 50 characters long.

#### Response:

```json
{
  "id": 1,
  "name": "John Doe"
}
```

---

### 2. `GET /participants`

This endpoint retrieves a list of all participants currently registered in the system.

#### Example:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/participants' \
  -H 'accept: application/json'
```

#### Response:

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

---

### 3. `POST /blacklist`

This endpoint allows one participant to blacklist another participant, preventing them from being paired together in the Secret Santa draw.

#### Example:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/blacklist' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"participant_id": 1, "blacklisted_participant_id": 2}'
```

#### Request Body:

```json
{
  "participant_id": 1,
  "blacklisted_participant_id": 2
}
```

- **`participant_id`**: The ID of the participant who is blacklisting another.
- **`blacklisted_participant_id`**: The ID of the participant being blacklisted.

#### Response:

```json
{
  "id": 1,
  "participant_id": 1,
  "blacklisted_participant_id": 2
}
```

---

### 4. `GET /draw`

This endpoint generates a valid Secret Santa draw, ensuring that all participants are paired with someone, and no one is paired with someone on their blacklist. The response now includes both the IDs and names of the gifter and the receiver.

#### Example:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/draw' \
  -H 'accept: application/json'
```

#### Response:

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

In this example John Doe is giving a gift to Jane Smith. Jane Smith is giving a gift to John Doe.

---

### 5. `POST /lists`

Create a new Secret Santa list. If no name is provided, one will be generated automatically using a Star Wars planet name.

#### Example:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/lists' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Holiday 2024"}'
```

#### Response:


```json
{
  "id": 1,
  "name": "Holiday 2024"
}
```


```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/lists' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}'
```


#### Response:


```json
{
  "id": 2,
  "name": "Tatooine-123456"
}
```

### 6. POST /lists/{list_id}/participants
Add a new participant to a specific Secret Santa list.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/lists/1/participants' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"name":"John Doe"}'
```

#### Response:

```json
{
  "id": 1,
  "name": "John Doe",
  "list_id": 1
}
```

### 7. GET /lists/{list_id}/participants
Retrieve all participants for a specific Secret Santa list.

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/lists/1/participants' \
  -H 'accept: application/json'
```

#### Response:

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

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/lists/1/draw' \
  -H 'accept: application/json'
```

#### Response:

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

## Running Tests

To run all unit tests for the API, execute the following command:

```bash
poetry run pytest
```

This will run all the tests to ensure the API's functionality is working as expected.

---

## Summary of Endpoints

- **POST `/participants`**: Add a new participant.
- **GET `/participants`**: Get a list of all participants.
- **POST `/blacklist`**: Add a participant to another participant's blacklist.
- **GET `/draw`**: Generate a valid Secret Santa draw, respecting blacklists.

## Important Resources

Here are some helpful links and resources related to the project:

[FastAPI Documentation](https://fastapi.tiangolo.com/)
[SQLModel Documentation](https://sqlmodel.tiangolo.com/)
[Poetry Documentation](https://python-poetry.org/docs/)
[Uvicorn Documentation](https://www.uvicorn.org/)
[Pytest Documentation](https://docs.pytest.org/en/stable/)


