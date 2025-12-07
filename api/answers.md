# Answers API

## Overview

The Answers API provides endpoints for managing answers to questions. Answers support moderation workflow and are broadcast to connected clients via Server-Sent Events (SSE).

## Base Path

`/answers`

---

## Endpoints

### POST /

**Description**: Create a new answer for a question. The answer is sent for moderation and broadcast to non-approved clients via SSE.

**Authentication**: Not required

**Request**:

- **Body**:

```json
{
  "answer": "string - The answer text (required)",
  "answeredBy": "string - User ID of the person answering (required)",
  "eventId": "string - Event ID associated with the answer (required)",
  "questionId": "string - Question ID this answer belongs to (required)"
}
```

**Mock Request Example**:

```json
{
  "answer": "JavaScript is my favorite programming language",
  "answeredBy": "user789",
  "eventId": "event456",
  "questionId": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response**:

- **Status Code**: 201
- **Body**:

```json
{
  "message": "Answer created and sent for moderation",
  "data": {
    "id": "string - Answer ID",
    "answer": "string - Answer text",
    "answeredBy": "string - User ID",
    "eventId": "string - Event ID",
    "questionId": "string - Question ID",
    "status": "string - Answer status (default: pending)",
    "createdAt": "timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Answer created and sent for moderation",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "answer": "JavaScript is my favorite programming language",
    "answeredBy": "user789",
    "eventId": "event456",
    "questionId": "550e8400-e29b-41d4-a716-446655440000",
    "status": "pending",
    "createdAt": "2024-01-15T10:35:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields)
- `500 Internal Server Error`: Server error

---

### PATCH /:answerId

**Description**: Update an answer, typically to change its moderation status. Updates are broadcast to connected clients via SSE based on their status filter.

**Authentication**: Required - SUPERUSER or MEMBER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `answerId`: string - The ID of the answer to update
- **Body**:

```json
{
  "status": "string - New status (optional, e.g., 'approved', 'rejected')"
}
```

**Mock Request Example**:

```json
{
  "status": "approved"
}
```

**Response**:

- **Status Code**: 204 (No Content)
- **Body**: Empty

**Error Responses**:

- `400 Bad Request`: Invalid payload
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER or MEMBER)
- `404 Not Found`: Answer not found
- `500 Internal Server Error`: Server error

**Notes**:

- The `reviewed_by` field is automatically set to the authenticated user's ID
- Approved answers are broadcast to clients with approved status filter
- All answers are broadcast to clients with non-approved status filter

---

### GET /

**Description**: Subscribe to answers via Server-Sent Events (SSE). Establishes a persistent connection to receive real-time answer updates. Can filter by status.

**Authentication**: Not required

**Request**:

- **Query Parameters**:
  - `status`: string (optional) - Filter answers by status (e.g., "approved")

**Response**:

- **Status Code**: 200
- **Content-Type**: `text/event-stream`
- **Headers**:
  - `Cache-Control: no-cache`
  - `Connection: keep-alive`
  - `X-Accel-Buffering: no`
- **Body**: SSE stream format
  - Initial connection: `data: null\n\n`
  - Subsequent updates: `data: [{answer objects}]\n\n`

**Mock Response Example** (SSE stream with status=approved):

```
data: null

data: [{"id":"660e8400-e29b-41d4-a716-446655440001","answer":"JavaScript is my favorite programming language","answeredBy":"user789","status":"approved"}]

```

**Error Responses**:

- `500 Internal Server Error`: Server error

**Notes**:

- This endpoint maintains a persistent connection
- Clients are automatically removed when connection closes
- Answers are filtered and broadcast based on the client's status preference
- Clients with approved status receive only approved answers
- Clients without approved status receive all answers
