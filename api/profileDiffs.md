# Profile Diffs API

## Overview

The Profile Diffs API provides endpoints for managing profile change requests. These are pending changes to user profiles that require approval from SUPERUSERs.

## Base Path

`/profileDiffs`

---

## Endpoints

### GET /

**Description**: Get profile diffs (pending profile changes). Supports pagination when dev flag is enabled.

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Query Parameters** (when dev flag is enabled):
  - `status`: string (optional, default: "PENDING") - Filter by status
  - `order`: string (optional, default: "desc") - Sort order: "asc" or "desc"
  - `size`: number (optional, default: 10) - Page size
  - `username`: string (optional, default: "") - Filter by username
  - `cursor`: string (optional) - Pagination cursor

**Response** (without dev flag):

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Profile Diffs returned successfully!",
  "profileDiffs": [
    {
      "id": "string - Diff ID",
      "userId": "string - User ID",
      "diff": {},
      "status": "string - Status",
      "createdAt": "timestamp"
    }
  ]
}
```

**Response** (with dev flag):

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Profile Diffs returned successfully!",
  "profileDiffs": [
    {
      "id": "string - Diff ID",
      "userId": "string - User ID",
      "diff": {},
      "status": "string - Status",
      "createdAt": "timestamp"
    }
  ],
  "next": "string - Next page cursor (if available)"
}
```

**Mock Request Example**:

- Path: `/profileDiffs?dev=true&status=PENDING&size=20`

**Mock Response Example**:

```json
{
  "message": "Profile Diffs returned successfully!",
  "profileDiffs": [
    {
      "id": "diff123",
      "userId": "user123",
      "diff": {
        "first_name": {
          "old": "John",
          "new": "Jonathan"
        }
      },
      "status": "PENDING",
      "createdAt": "2024-01-15T10:00:00Z"
    }
  ],
  "next": "cursor456"
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `503 Service Unavailable`: Server error

---

### GET /:id

**Description**: Get a specific profile diff by ID

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `id`: string - Profile diff ID

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Profile Diff returned successfully!",
  "profileDiff": {
    "id": "string - Diff ID",
    "userId": "string - User ID",
    "diff": {},
    "status": "string - Status",
    "createdAt": "timestamp"
  }
}
```

**Mock Request Example**:

- Path: `/profileDiffs/diff123`

**Mock Response Example**:

```json
{
  "message": "Profile Diff returned successfully!",
  "profileDiff": {
    "id": "diff123",
    "userId": "user123",
    "diff": {
      "first_name": {
        "old": "John",
        "new": "Jonathan"
      },
      "last_name": {
        "old": "Doe",
        "new": "Smith"
      }
    },
    "status": "PENDING",
    "createdAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `404 Not Found`: Profile diff doesn't exist
- `503 Service Unavailable`: Server error
