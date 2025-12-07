# Questions API

## Overview

The Questions API provides endpoints for managing questions, particularly for real-time word cloud features. Questions are sent to connected clients via Server-Sent Events (SSE).

## Base Path

`/questions`

---

## Endpoints

### POST /

**Description**: Create a new question and broadcast it to all connected clients via SSE

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "question": "string - The question text (required)",
  "createdBy": "string - User ID of the creator (required)",
  "eventId": "string - Event ID associated with the question (required)",
  "maxCharacters": "number - Maximum characters allowed (optional)"
}
```

**Mock Request Example**:

```json
{
  "question": "What is your favorite programming language?",
  "createdBy": "user123",
  "eventId": "event456",
  "maxCharacters": 100
}
```

**Response**:

- **Status Code**: 201
- **Body**:

```json
{
  "message": "Question created and sent successfully to connected peers",
  "data": {
    "id": "string - Question ID",
    "question": "string - Question text",
    "createdBy": "string - Creator user ID",
    "eventId": "string - Event ID",
    "maxCharacters": "number - Max characters",
    "createdAt": "timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Question created and sent successfully to connected peers",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "question": "What is your favorite programming language?",
    "createdBy": "user123",
    "eventId": "event456",
    "maxCharacters": 100,
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### GET /

**Description**: Subscribe to questions via Server-Sent Events (SSE). Establishes a persistent connection to receive real-time question updates.

**Authentication**: Not required

**Request**:

- No parameters required
- This endpoint uses Server-Sent Events (SSE) protocol

**Response**:

- **Status Code**: 200
- **Content-Type**: `text/event-stream`
- **Headers**:
  - `Cache-Control: no-cache`
  - `Connection: keep-alive`
  - `X-Accel-Buffering: no`
- **Body**: SSE stream format
  - Initial connection: `data: null\n\n`
  - Subsequent updates: `data: {question object}\n\n`

**Mock Response Example** (SSE stream):

```
data: null

data: {"id":"550e8400-e29b-41d4-a716-446655440000","question":"What is your favorite programming language?","createdBy":"user123","eventId":"event456"}

```

**Error Responses**:

- `500 Internal Server Error`: Server error

**Notes**:

- This endpoint maintains a persistent connection
- Clients are automatically removed when connection closes
- Questions are broadcast to all connected clients in real-time
