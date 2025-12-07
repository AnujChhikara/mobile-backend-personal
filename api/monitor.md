# Monitor API

## Overview

The Monitor API provides endpoints for tracking and monitoring progress of users and tasks. It allows creating, updating, and retrieving tracked progress records.

## Base Path

`/monitor`

---

## Endpoints

### POST /

**Description**: Create a new tracked progress record for monitoring a user or task

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "type": "string - Type of tracked progress: 'user' or 'task' (required)",
  "userId": "string - User ID (required if type is 'user')",
  "taskId": "string - Task ID (required if type is 'task')",
  "monitored": "boolean - Whether the progress is currently being tracked (required)",
  "frequency": "number - Frequency of tracking (optional, default: 1)"
}
```

**Mock Request Example** (user type):

```json
{
  "type": "user",
  "userId": "user123",
  "monitored": true,
  "frequency": 1
}
```

**Mock Request Example** (task type):

```json
{
  "type": "task",
  "taskId": "task456",
  "monitored": true,
  "frequency": 2
}
```

**Response**:

- **Status Code**: 201
- **Body**:

```json
{
  "message": "Resource created successfully",
  "data": {
    "id": "string - Tracked progress ID",
    "type": "string - Type ('user' or 'task')",
    "userId": "string - User ID (if type is 'user')",
    "taskId": "string - Task ID (if type is 'task')",
    "monitored": "boolean - Monitoring status",
    "frequency": "number - Tracking frequency",
    "createdAt": "timestamp - Creation timestamp",
    "updatedAt": "timestamp - Last update timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Resource created successfully",
  "data": {
    "id": "monitor1",
    "type": "user",
    "userId": "user123",
    "monitored": true,
    "frequency": 1,
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `404 Not Found`: User or task not found
- `409 Conflict`: Tracked progress record already exists
- `500 Internal Server Error`: Server error

---

### PATCH /:type/:typeId

**Description**: Update an existing tracked progress record

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `type`: string - Type of tracked progress: 'user' or 'task'
  - `typeId`: string - The ID of the user or task being tracked
- **Body**:

```json
{
  "frequency": "number - Frequency of tracking (optional)",
  "monitored": "boolean - Whether the progress is currently being tracked (optional)"
}
```

**Mock Request Example**:

- Path: `/monitor/user/user123`
- Body:

```json
{
  "monitored": false,
  "frequency": 2
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Resource updated successfully",
  "data": {
    "id": "string - Tracked progress ID",
    "type": "string - Type ('user' or 'task')",
    "userId": "string - User ID (if type is 'user')",
    "taskId": "string - Task ID (if type is 'task')",
    "monitored": "boolean - Monitoring status",
    "frequency": "number - Tracking frequency",
    "createdAt": "timestamp - Creation timestamp",
    "updatedAt": "timestamp - Last update timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Resource updated successfully",
  "data": {
    "id": "monitor1",
    "type": "user",
    "userId": "user123",
    "monitored": false,
    "frequency": 2,
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `404 Not Found`: Tracked progress record not found
- `500 Internal Server Error`: Server error

---

### GET /

**Description**: Get tracked progress records with optional filtering

**Authentication**: Not required

**Request**:

- **Query Parameters**:
  - `type`: string (optional) - Filter by type ('user' or 'task')
  - `monitored`: string (optional) - Filter by monitoring status ('true' or 'false')
  - `userId`: string (optional) - Filter by user ID
  - `taskId`: string (optional) - Filter by task ID

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Resource retrieved successfully",
  "data": [
    {
      "id": "string - Tracked progress ID",
      "type": "string - Type ('user' or 'task')",
      "userId": "string - User ID (if type is 'user')",
      "taskId": "string - Task ID (if type is 'task')",
      "monitored": "boolean - Monitoring status",
      "frequency": "number - Tracking frequency",
      "createdAt": "timestamp - Creation timestamp",
      "updatedAt": "timestamp - Last update timestamp"
    }
  ]
}
```

**Mock Request Example**:

- Path: `/monitor?type=user&monitored=true`

**Mock Response Example** (array):

```json
{
  "message": "Resource retrieved successfully",
  "data": [
    {
      "id": "monitor1",
      "type": "user",
      "userId": "user123",
      "monitored": true,
      "frequency": 1,
      "createdAt": "2024-01-15T10:00:00Z",
      "updatedAt": "2024-01-15T10:00:00Z"
    },
    {
      "id": "monitor2",
      "type": "user",
      "userId": "user456",
      "monitored": true,
      "frequency": 1,
      "createdAt": "2024-01-15T10:05:00Z",
      "updatedAt": "2024-01-15T10:05:00Z"
    }
  ]
}
```

**Mock Response Example** (single object when filtered):

```json
{
  "message": "Resource retrieved successfully",
  "data": {
    "id": "monitor1",
    "type": "user",
    "userId": "user123",
    "monitored": true,
    "frequency": 1,
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid query parameters
- `404 Not Found`: No records found (when type filter is provided)
- `500 Internal Server Error`: Server error
