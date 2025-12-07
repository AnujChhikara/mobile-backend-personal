# Tags API

## Overview

The Tags API provides endpoints for managing tags that can be associated with various entities in the system. Tags are categorized by type.

## Base Path

`/tags`

---

## Endpoints

### GET /

**Description**: Get all tags in the system

**Authentication**: Not required

**Request**:

- No parameters required

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Tags returned successfully",
  "tags": [
    {
      "id": "string - Tag ID",
      "name": "string - Tag name",
      "type": "string - Tag type",
      "reason": "string - Reason for tag creation",
      "createdBy": "string - Creator user ID",
      "date": "timestamp - Creation date"
    }
  ]
}
```

**Mock Response Example**:

```json
{
  "message": "Tags returned successfully",
  "tags": [
    {
      "id": "tag123",
      "name": "JavaScript",
      "type": "SKILL",
      "reason": "Programming language skill",
      "createdBy": "user456",
      "date": "2024-01-15T10:00:00Z"
    },
    {
      "id": "tag124",
      "name": "React",
      "type": "SKILL",
      "reason": "Frontend framework",
      "createdBy": "user456",
      "date": "2024-01-15T10:05:00Z"
    }
  ]
}
```

**Error Responses**:

- `500 Internal Server Error`: Server error

---

### GET /:type

**Description**: Get all tags filtered by type

**Authentication**: Not required

**Request**:

- **Path Parameters**:
  - `type`: string - Tag type (case-insensitive, will be converted to uppercase)

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Tags of type: {TYPE} returned successfully",
  "tags": [
    {
      "id": "string - Tag ID",
      "name": "string - Tag name",
      "type": "string - Tag type",
      "reason": "string - Reason for tag creation",
      "createdBy": "string - Creator user ID",
      "date": "timestamp - Creation date"
    }
  ]
}
```

**Mock Request Example**:

- Path: `/tags/skill`

**Mock Response Example**:

```json
{
  "message": "Tags of type: SKILL returned successfully",
  "tags": [
    {
      "id": "tag123",
      "name": "JavaScript",
      "type": "SKILL",
      "reason": "Programming language skill",
      "createdBy": "user456",
      "date": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Error Responses**:

- `500 Internal Server Error`: Server error

---

### POST /

**Description**: Create a new tag

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "name": "string - Tag name (required, trimmed)",
  "type": "string - Tag type (required, must be one of valid types, will be uppercased)",
  "reason": "string - Reason for tag creation (optional)"
}
```

**Mock Request Example**:

```json
{
  "name": "TypeScript",
  "type": "skill",
  "reason": "Programming language with type safety"
}
```

**Response**:

- **Status Code**: 200 (if tag created) or 400 (if tag already exists)
- **Body** (Success):

```json
{
  "message": "Tag created successfully",
  "data": {
    "tag": {
      "name": "string - Tag name",
      "type": "string - Tag type",
      "reason": "string - Reason",
      "createdBy": "string - Creator user ID",
      "date": "timestamp"
    },
    "id": "string - Tag ID"
  }
}
```

**Mock Response Example** (Success):

```json
{
  "message": "Tag created successfully",
  "data": {
    "tag": {
      "name": "TypeScript",
      "type": "SKILL",
      "reason": "Programming language with type safety",
      "createdBy": "user456",
      "date": "2024-01-15T10:10:00Z"
    },
    "id": "tag125"
  }
}
```

**Mock Response Example** (Tag already exists):

```json
{
  "message": "Tag already exists",
  "data": {
    "tag": {
      "name": "TypeScript",
      "type": "SKILL"
    }
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload or tag already exists
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### DELETE /:tagid

**Description**: Delete a tag by ID

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `tagid`: string - The ID of the tag to delete

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Tag Deleted successfully!",
  "id": "string - Deleted tag ID"
}
```

**Mock Request Example**:

- Path: `/tags/tag123`

**Mock Response Example**:

```json
{
  "message": "Tag Deleted successfully!",
  "id": "tag123"
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `404 Not Found`: Tag not found
- `500 Internal Server Error`: Server error
