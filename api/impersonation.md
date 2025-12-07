# Impersonation API

## Overview

The Impersonation API provides endpoints for managing user impersonation requests. This allows SUPERUSERs to temporarily act as another user for support and debugging purposes. This feature is only available in development environments.

## Base Path

`/impersonation`

**Note**: This API requires dev flag to be enabled and is restricted to SUPERUSER role.

---

## Endpoints

### POST /requests

**Description**: Create a new impersonation request

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "createdFor": "string - User ID to impersonate (required)",
  "reason": "string - Reason for impersonation (required)"
}
```

**Mock Request Example**:

```json
{
  "createdFor": "user123",
  "reason": "Debugging user issue with profile updates"
}
```

**Response**:

- **Status Code**: 201
- **Body**:

```json
{
  "message": "Request created successfully",
  "data": {
    "id": "string - Request ID",
    "createdBy": "string - Creator user ID",
    "createdFor": "string - Target user ID",
    "reason": "string - Reason",
    "status": "string - Status: PENDING, APPROVED, or REJECTED",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Request created successfully",
  "data": {
    "id": "req123",
    "createdBy": "superuser456",
    "createdFor": "user123",
    "reason": "Debugging user issue with profile updates",
    "status": "PENDING",
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields or empty strings)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### GET /requests

**Description**: Get impersonation requests with optional filtering and pagination

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Query Parameters**:
  - `createdBy`: string (optional) - Filter by creator user ID (case-insensitive)
  - `createdFor`: string (optional) - Filter by target user ID (case-insensitive)
  - `status`: string (optional) - Filter by status: "APPROVED", "PENDING", or "REJECTED"
  - `next`: string (optional) - Cursor for next page
  - `prev`: string (optional) - Cursor for previous page
  - `size`: number (optional) - Page size (1-100, default varies)
  - `dev`: string (optional) - Dev flag

**Response**:

- **Status Code**: 200 (with data) or 204 (no content)
- **Body** (with data):

```json
{
  "message": "Request fetched successfully",
  "data": [
    {
      "id": "string - Request ID",
      "createdBy": "string - Creator user ID",
      "createdFor": "string - Target user ID",
      "reason": "string - Reason",
      "status": "string - Status",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "next": "string - URL for next page (if available)",
  "prev": "string - URL for previous page (if available)",
  "count": "number - Total count"
}
```

**Mock Request Example**:

- Path: `/impersonation/requests?status=PENDING&size=10`

**Mock Response Example**:

```json
{
  "message": "Request fetched successfully",
  "data": [
    {
      "id": "req123",
      "createdBy": "superuser456",
      "createdFor": "user123",
      "reason": "Debugging user issue",
      "status": "PENDING",
      "createdAt": "2024-01-15T10:00:00Z",
      "updatedAt": "2024-01-15T10:00:00Z"
    }
  ],
  "next": null,
  "prev": null,
  "count": 1
}
```

**Error Responses**:

- `400 Bad Request`: Invalid query parameters
- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error

---

### GET /requests/:id

**Description**: Get a specific impersonation request by ID

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `id`: string (required) - Request ID (alphanumeric, dashes, underscores, max 100 chars)

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Request fetched successfully",
  "data": {
    "id": "string - Request ID",
    "createdBy": "string - Creator user ID",
    "createdFor": "string - Target user ID",
    "reason": "string - Reason",
    "status": "string - Status",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
}
```

**Mock Request Example**:

- Path: `/impersonation/requests/req123`

**Mock Response Example**:

```json
{
  "message": "Request fetched successfully",
  "data": {
    "id": "req123",
    "createdBy": "superuser456",
    "createdFor": "user123",
    "reason": "Debugging user issue",
    "status": "PENDING",
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid request ID format
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Request not found
- `500 Internal Server Error`: Server error

---

### PATCH /requests/:id

**Description**: Update the status of an impersonation request (approve or reject)

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `id`: string - Request ID
- **Body**:

```json
{
  "status": "string - New status: 'APPROVED' or 'REJECTED' (required)",
  "message": "string - Optional message (optional)"
}
```

**Mock Request Example**:

```json
{
  "status": "APPROVED",
  "message": "Approved for debugging session"
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "string - Success message",
  "data": {
    "id": "string - Request ID",
    "createdBy": "string - Creator user ID",
    "createdFor": "string - Target user ID",
    "reason": "string - Reason",
    "status": "string - Updated status",
    "lastModifiedBy": "string - User ID who updated",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Request status updated successfully",
  "data": {
    "id": "req123",
    "createdBy": "superuser456",
    "createdFor": "user123",
    "reason": "Debugging user issue",
    "status": "APPROVED",
    "lastModifiedBy": "superuser789",
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (invalid status or missing required fields)
- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error

---

### PATCH /:id

**Description**: Start or stop an impersonation session. This sets/clears the impersonation cookie.

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `id`: string - Request ID
- **Query Parameters**:
  - `action`: string (required) - Action to perform: "START" or "STOP"
  - `dev`: string (optional) - Dev flag

**Response**:

- **Status Code**: 200
- **Headers**: Sets/clears impersonation cookie
- **Body**:

```json
{
  "message": "string - Success message",
  "data": {
    "id": "string - Request ID",
    "createdBy": "string - Creator user ID",
    "createdFor": "string - Target user ID",
    "status": "string - Status",
    "sessionStartedAt": "timestamp - When session started (if START)",
    "sessionEndedAt": "timestamp - When session ended (if STOP)",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
}
```

**Mock Request Example**:

- Path: `/impersonation/req123?action=START`

**Mock Response Example** (START):

```json
{
  "message": "Impersonation session started successfully",
  "data": {
    "id": "req123",
    "createdBy": "superuser456",
    "createdFor": "user123",
    "status": "APPROVED",
    "sessionStartedAt": "2024-01-15T10:35:00Z",
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:35:00Z"
  }
}
```

**Mock Response Example** (STOP):

```json
{
  "message": "Impersonation session stopped successfully",
  "data": {
    "id": "req123",
    "createdBy": "superuser456",
    "createdFor": "user123",
    "status": "APPROVED",
    "sessionStartedAt": "2024-01-15T10:35:00Z",
    "sessionEndedAt": "2024-01-15T11:00:00Z",
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T11:00:00Z"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid action (must be START or STOP)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Cannot START without approved request or cannot STOP without active session
- `404 Not Found`: Request not found
- `500 Internal Server Error`: Server error

**Notes**:

- START action requires the request to be in APPROVED status
- STOP action requires an active impersonation session
- The impersonation cookie is automatically set/cleared based on the action
- Impersonation tokens have a shorter TTL (15 minutes by default)
