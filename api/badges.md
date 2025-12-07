# Badges API

## Overview

The Badges API provides endpoints for managing badges and assigning them to users. Badges are achievements or recognitions that can be displayed on user profiles.

## Base Path

`/badges`

---

## Endpoints

### GET /

**Description**: Get all badges in the system

**Authentication**: Not required

**Request**:

- **Query Parameters**: (optional, varies based on implementation)

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Badges returned successfully",
  "badges": [
    {
      "id": "string - Badge ID",
      "name": "string - Badge name",
      "description": "string - Badge description",
      "imageUrl": "string - Badge image URL",
      "createdBy": "string - Creator user ID",
      "createdAt": "timestamp"
    }
  ]
}
```

**Mock Response Example**:

```json
{
  "message": "Badges returned successfully",
  "badges": [
    {
      "id": "badge1",
      "name": "Early Contributor",
      "description": "Awarded to early contributors",
      "imageUrl": "https://example.com/badge1.png",
      "createdBy": "admin123",
      "createdAt": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**Error Responses**:

- `400 Bad Request`: Error fetching badges
- `500 Internal Server Error`: Server error

---

### POST /

**Description**: Create a new badge

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
  - `Content-Type`: multipart/form-data
- **Body** (form-data):
  - `file`: File (required) - Badge image file
  - `name`: string (required, 3-30 chars) - Badge name
  - `description`: string (optional, 3-130 chars) - Badge description
  - `createdBy`: string (required) - Creator user ID

**Mock Request Example**:

- Form data with file upload
- name: "Early Contributor"
- description: "Awarded to early contributors"
- createdBy: "admin123"

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Badge created successfully",
  "badge": {
    "id": "string - Badge ID",
    "name": "string - Badge name",
    "description": "string - Badge description",
    "imageUrl": "string - Uploaded image URL",
    "createdBy": "string - Creator user ID",
    "createdAt": "timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Badge created successfully",
  "badge": {
    "id": "badge1",
    "name": "Early Contributor",
    "description": "Awarded to early contributors",
    "imageUrl": "https://cloudinary.com/badge1.png",
    "createdBy": "admin123",
    "createdAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing file, invalid name length, etc.)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### POST /assign

**Description**: Assign badges to a user

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "userId": "string - User ID (required)",
  "badgeIds": ["string - Badge ID (required, min 1, unique)"]
}
```

**Mock Request Example**:

```json
{
  "userId": "user123",
  "badgeIds": ["badge1", "badge2"]
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Badges assigned successfully"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing userId, empty badgeIds, duplicate badgeIds, or user doesn't exist)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

**Notes**:

- Badge IDs are not validated for existence
- Same badge can be assigned multiple times (no duplicate check)

---

### DELETE /remove

**Description**: Remove badges from a user

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "userId": "string - User ID (required)",
  "badgeIds": ["string - Badge ID (required, min 1, unique)"]
}
```

**Mock Request Example**:

```json
{
  "userId": "user123",
  "badgeIds": ["badge1"]
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Badges removed successfully"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing userId, empty badgeIds, duplicate badgeIds)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error
