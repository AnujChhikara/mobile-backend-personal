# Levels API

## Overview

The Levels API provides endpoints for managing user levels in the system. Levels represent progression tiers with numeric values.

## Base Path

`/levels`

---

## Endpoints

### GET /

**Description**: Get all levels in the system

**Authentication**: Not required

**Request**:

- No parameters required

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Levels returned Successfully",
  "levels": [
    {
      "id": "string - Level ID",
      "name": "string - Level name",
      "value": "number - Level numeric value",
      "createdBy": "string - Creator user ID",
      "date": "timestamp - Creation date"
    }
  ]
}
```

**Mock Response Example**:

```json
{
  "message": "Levels returned Successfully",
  "levels": [
    {
      "id": "level1",
      "name": "Beginner",
      "value": 1,
      "createdBy": "user456",
      "date": "2024-01-15T10:00:00Z"
    },
    {
      "id": "level2",
      "name": "Intermediate",
      "value": 2,
      "createdBy": "user456",
      "date": "2024-01-15T10:05:00Z"
    },
    {
      "id": "level3",
      "name": "Advanced",
      "value": 3,
      "createdBy": "user456",
      "date": "2024-01-15T10:10:00Z"
    }
  ]
}
```

**Error Responses**:

- `500 Internal Server Error`: Server error

---

### POST /

**Description**: Create a new level

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "name": "string - Level name (required, trimmed)",
  "value": "number - Level numeric value (required, integer, min: 0)"
}
```

**Mock Request Example**:

```json
{
  "name": "Expert",
  "value": 4
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Level created successfully!",
  "data": {
    "level": {
      "name": "string - Level name",
      "value": "number - Level value",
      "createdBy": "string - Creator user ID",
      "date": "timestamp"
    },
    "id": "string - Level ID"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Level created successfully!",
  "data": {
    "level": {
      "name": "Expert",
      "value": 4,
      "createdBy": "user456",
      "date": "2024-01-15T10:15:00Z"
    },
    "id": "level4"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields or invalid value)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### DELETE /:levelid

**Description**: Delete a level by ID

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `levelid`: string - The ID of the level to delete

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Level Deleted successfully!"
}
```

**Mock Request Example**:

- Path: `/levels/level1`

**Mock Response Example**:

```json
{
  "message": "Level Deleted successfully!"
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `404 Not Found`: Level not found
- `500 Internal Server Error`: Server error
