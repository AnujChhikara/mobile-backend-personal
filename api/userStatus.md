# User Status API

## Overview

The User Status API provides endpoints for managing user statuses including ACTIVE, IDLE, OOO (Out of Office), and ONBOARDING states. It supports status updates, batch operations, and aggregation queries.

## Base Path

`/users/status`

---

## Endpoints

### GET /

**Description**: Get all user statuses with optional filtering. Can also aggregate user statuses based on tasks.

**Authentication**: Not required

**Request**:

- **Query Parameters**:
  - `aggregate`: boolean (optional) - If true, returns task-based user status aggregation
  - `state`: string (optional) - Filter by state: "IDLE", "ACTIVE", "OOO", or "ONBOARDING"

**Response** (without aggregate):

- **Status Code**: 200
- **Body**:

```json
{
  "message": "All User Status found successfully.",
  "totalUserStatus": "number - Total count",
  "allUserStatus": [
    {
      "userId": "string - User ID",
      "currentStatus": {
        "state": "string - State (ACTIVE, IDLE, OOO, ONBOARDING)",
        "updatedAt": "number - Timestamp",
        "from": "number - Start timestamp",
        "until": "number - End timestamp (for OOO)",
        "message": "string - Status message"
      },
      "monthlyHours": {
        "committed": "number - Committed hours",
        "updatedAt": "number - Timestamp"
      },
      "full_name": "string - User full name",
      "picture": "string - User picture URL",
      "username": "string - Username"
    }
  ]
}
```

**Response** (with aggregate=true):

- **Status Code**: 200
- **Body**:

```json
{
  "message": "All users based on tasks found successfully.",
  "data": {}
}
```

**Mock Request Example**:

- Path: `/users/status?state=OOO`

**Mock Response Example**:

```json
{
  "message": "All User Status found successfully.",
  "totalUserStatus": 2,
  "allUserStatus": [
    {
      "userId": "user123",
      "currentStatus": {
        "state": "OOO",
        "updatedAt": 1705320000000,
        "from": 1705320000000,
        "until": 1705507200000,
        "message": "Vacation"
      },
      "monthlyHours": {
        "committed": 40,
        "updatedAt": 1705320000000
      },
      "full_name": "John Doe",
      "picture": "https://example.com/pic.jpg",
      "username": "johndoe"
    }
  ]
}
```

**Error Responses**:

- `400 Bad Request`: Invalid query parameters
- `500 Internal Server Error`: Server error

---

### GET /self

**Description**: Get the authenticated user's status

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}

**Response**:

- **Status Code**: 200 (found) or 404 (not found)
- **Body** (found):

```json
{
  "message": "User Status found successfully.",
  "id": "string - Status document ID",
  "userId": "string - User ID",
  "data": {
    "currentStatus": {
      "state": "string - State",
      "updatedAt": "number - Timestamp",
      "from": "number - Start timestamp",
      "until": "number - End timestamp",
      "message": "string - Status message"
    },
    "monthlyHours": {
      "committed": "number - Committed hours",
      "updatedAt": "number - Timestamp"
    }
  }
}
```

**Mock Response Example**:

```json
{
  "message": "User Status found successfully.",
  "id": "status123",
  "userId": "user123",
  "data": {
    "currentStatus": {
      "state": "ACTIVE",
      "updatedAt": 1705320000000,
      "from": 1705320000000,
      "message": ""
    },
    "monthlyHours": {
      "committed": 40,
      "updatedAt": 1705320000000
    }
  }
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `404 Not Found`: User status not found
- `500 Internal Server Error`: Server error

---

### GET /:userId

**Description**: Get a specific user's status by user ID

**Authentication**: Not required

**Request**:

- **Path Parameters**:
  - `userId`: string - The ID of the user

**Response**:

- **Status Code**: 200 (found) or 404 (not found)
- **Body**: Same format as GET /self

**Mock Request Example**:

- Path: `/users/status/user123`

**Error Responses**:

- `404 Not Found`: User status not found
- `500 Internal Server Error`: Server error

---

### PATCH /self

**Description**: Update the authenticated user's status. Supports setting OOO, ONBOARDING states or canceling OOO status.

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body** (for status update):

```json
{
  "currentStatus": {
    "state": "string - State: 'OOO' or 'ONBOARDING' (required)",
    "updatedAt": "number - Timestamp (required)",
    "from": "number - Start timestamp (required, must be today or future)",
    "until": "number - End timestamp (required for OOO, must be >= from)",
    "message": "string - Status message (required for OOO, optional for ONBOARDING)"
  },
  "monthlyHours": {
    "committed": "number - Committed hours (required)",
    "updatedAt": "number - Timestamp (required)"
  }
}
```

**Body** (for canceling OOO):

```json
{
  "cancelOoo": true
}
```

**Mock Request Example** (setting OOO):

```json
{
  "currentStatus": {
    "state": "OOO",
    "updatedAt": 1705320000000,
    "from": 1705320000000,
    "until": 1705507200000,
    "message": "Vacation"
  },
  "monthlyHours": {
    "committed": 40,
    "updatedAt": 1705320000000
  }
}
```

**Response**:

- **Status Code**: 200 (updated) or 201 (created)
- **Body**:

```json
{
  "message": "User Status updated successfully." | "User Status created successfully.",
  "id": "string - Status document ID",
  "userId": "string - User ID",
  "data": {
    "currentStatus": {},
    "monthlyHours": {}
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (invalid state, dates, or missing required fields)
- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error

**Notes**:

- This route is being deprecated. Use `/users/status/:userId` PATCH endpoint instead.
- For OOO status longer than 3 days, message is mandatory
- The 'from' field must be today or a future date
- The 'until' field must be >= 'from' date

---

### PATCH /:userId

**Description**: Update a specific user's status. Users can only update their own status unless they are SUPERUSER.

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `userId`: string - The ID of the user whose status to update
- **Body**: Same format as PATCH /self

**Response**:

- **Status Code**: 200 (updated) or 201 (created)
- **Body**: Same format as PATCH /self

**Mock Request Example**:

- Path: `/users/status/user123`
- Body: Same as PATCH /self example

**Error Responses**:

- `400 Bad Request`: Invalid payload
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not authorized to update this user's status
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server error

**Notes**:

- Users can only update their own status
- SUPERUSER can update any user's status

---

### PATCH /update

**Description**: Update all user statuses (internal/cron job endpoint)

**Authentication**: Required - SUPERUSER role or CRON_JOB_HANDLER service

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env} (if user)
  - Service authentication (if service)

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "All User Status updated successfully.",
  "data": {}
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Server error

---

### PATCH /batch

**Description**: Batch update user statuses for multiple users

**Authentication**: Required - SUPERUSER role or CRON_JOB_HANDLER service

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env} (if user)
  - Service authentication (if service)
- **Body**:

```json
{
  "users": [
    {
      "userId": "string - User ID (required)",
      "state": "string - State: 'IDLE' or 'ACTIVE' (required)"
    }
  ]
}
```

**Mock Request Example**:

```json
{
  "users": [
    {
      "userId": "user123",
      "state": "IDLE"
    },
    {
      "userId": "user456",
      "state": "ACTIVE"
    }
  ]
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "users status updated successfully.",
  "data": {}
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (empty users array or invalid state)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Server error

---

### DELETE /:userId

**Description**: Delete a user's status

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `userId`: string - The ID of the user whose status to delete

**Response**:

- **Status Code**: 200 (deleted) or 404 (not found)
- **Body**:

```json
{
  "message": "User Status deleted successfully." | "User Status to delete not found.",
  "id": "string - Deleted status document ID",
  "userId": "string - User ID"
}
```

**Mock Request Example**:

- Path: `/users/status/user123`

**Mock Response Example**:

```json
{
  "message": "User Status deleted successfully.",
  "id": "status123",
  "userId": "user123"
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error
