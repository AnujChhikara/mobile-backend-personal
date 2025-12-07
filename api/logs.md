# Logs API

## Overview

The Logs API provides endpoints for fetching and managing system logs. Logs can be filtered by type and support pagination.

## Base Path

`/logs`

---

## Endpoints

### GET /

**Description**: Get all logs with pagination support

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Query Parameters**:
  - `page`: number (optional) - Page number for pagination
  - `next`: string (optional) - Cursor for next page
  - `prev`: string (optional) - Cursor for previous page

**Response**:

- **Status Code**: 200 (with data) or 204 (no content)
- **Body** (with pagination links):

```json
{
  "message": "All logs fetched successfully",
  "data": [
    {
      "id": "string - Log ID",
      "type": "string - Log type",
      "message": "string - Log message",
      "timestamp": "timestamp",
      "metadata": {}
    }
  ],
  "next": "string - URL for next page (if available)",
  "prev": "string - URL for previous page (if available)"
}
```

**Body** (with page number):

```json
{
  "message": "All logs fetched successfully",
  "data": [
    {
      "id": "string - Log ID",
      "type": "string - Log type",
      "message": "string - Log message",
      "timestamp": "timestamp",
      "metadata": {}
    }
  ],
  "page": "string - URL for current page"
}
```

**Mock Response Example** (with pagination):

```json
{
  "message": "All logs fetched successfully",
  "data": [
    {
      "id": "log1",
      "type": "error",
      "message": "Database connection failed",
      "timestamp": "2024-01-15T10:00:00Z",
      "metadata": {
        "userId": "user123"
      }
    },
    {
      "id": "log2",
      "type": "info",
      "message": "User logged in",
      "timestamp": "2024-01-15T10:05:00Z",
      "metadata": {
        "userId": "user456"
      }
    }
  ],
  "next": "/logs?next=cursor123",
  "prev": null
}
```

**Mock Response Example** (no content):

- Status: 204 No Content
- Body: Empty

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### GET /:type

**Description**: Get logs filtered by type

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `type`: string - Log type to filter by
- **Query Parameters**:
  - Additional query parameters may be supported for filtering

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Logs fetched successfully",
  "logs": [
    {
      "id": "string - Log ID",
      "type": "string - Log type",
      "message": "string - Log message",
      "timestamp": "timestamp",
      "metadata": {}
    }
  ]
}
```

**Mock Request Example**:

- Path: `/logs/error`

**Mock Response Example**:

```json
{
  "message": "Logs fetched successfully",
  "logs": [
    {
      "id": "log1",
      "type": "error",
      "message": "Database connection failed",
      "timestamp": "2024-01-15T10:00:00Z",
      "metadata": {
        "userId": "user123"
      }
    },
    {
      "id": "log3",
      "type": "error",
      "message": "API rate limit exceeded",
      "timestamp": "2024-01-15T10:10:00Z",
      "metadata": {
        "endpoint": "/api/users"
      }
    }
  ]
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### POST /migrate

**Description**: Migrate or update logs (internal operation)

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**: (varies based on migration requirements)

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "response": "string - Migration response message"
}
```

**Mock Response Example**:

```json
{
  "response": "Logs migration completed successfully"
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `503 Service Unavailable`: Server error during migration
