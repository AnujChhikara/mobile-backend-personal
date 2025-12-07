# External Accounts API

## Overview

The External Accounts API provides endpoints for managing external account integrations, particularly Discord account linking and synchronization.

## Base Path

`/external-accounts`

---

## Endpoints

### POST /

**Description**: Add external account data (typically called by Discord bot)

**Authentication**: Required - Discord Bot verification

**Request**:

- **Headers**:
  - Discord bot authentication token
- **Body**:

```json
{
  "token": "string - Unique token (required)",
  "attributes": {
    "discordId": "string - Discord user ID",
    "discordJoinedAt": "timestamp - Discord join timestamp",
    "expiry": "number - Token expiry timestamp (optional)"
  }
}
```

**Mock Request Example**:

```json
{
  "token": "unique-token-123",
  "attributes": {
    "discordId": "discord123",
    "discordJoinedAt": 1705320000000,
    "expiry": 1705507200000
  }
}
```

**Response**:

- **Status Code**: 201
- **Body**:

```json
{
  "message": "Added external account data successfully"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload
- `401 Unauthorized`: Invalid bot authentication
- `409 Conflict`: Token already exists
- `503 Service Unavailable`: Server error

---

### GET /:token

**Description**: Get external account data by token

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `token`: string - External account token
- **Query Parameters**: (optional, varies)

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Data returned successfully",
  "attributes": {
    "discordId": "string - Discord user ID",
    "discordJoinedAt": "timestamp - Discord join timestamp",
    "expiry": "number - Token expiry timestamp"
  }
}
```

**Mock Request Example**:

- Path: `/external-accounts/unique-token-123`

**Mock Response Example**:

```json
{
  "message": "Data returned successfully",
  "attributes": {
    "discordId": "discord123",
    "discordJoinedAt": 1705320000000,
    "expiry": 1705507200000
  }
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated or token expired
- `404 Not Found`: No data found for token
- `503 Service Unavailable`: Server error

**Notes**:

- If token has expiry and it's expired, returns 401 Unauthorized

---

### PATCH /link/:token

**Description**: Link external account (Discord) to the authenticated user

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `token`: string - External account token

**Response**:

- **Status Code**: 204
- **Body**:

```json
{
  "message": "Your discord profile has been linked successfully"
}
```

**Mock Request Example**:

- Path: `/external-accounts/link/unique-token-123`

**Mock Response Example**:

```json
{
  "message": "Your discord profile has been linked successfully"
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated or token expired
- `404 Not Found`: No data found for token
- `500 Internal Server Error`: Error removing Discord unverified role
- `503 Service Unavailable`: Server error

**Notes**:

- Updates user's Discord ID and sets `in_discord: true` and `archived: false`
- Removes unverified Discord role from user
- If role removal fails, returns error but user details are still updated

---

### PATCH /discord-sync

**Description**: Sync external account data from Discord (deprecated)

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}

**Response**:

- **Status Code**: 200
- **Body**: (varies)

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `503 Service Unavailable`: Server error

**Notes**:

- This endpoint is deprecated

---

### POST /users

**Description**: Handle external accounts user operations (internal/cron job endpoint)

**Authentication**: Required - SUPERUSER role or CRON_JOB_HANDLER service

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env} (if user)
  - Service authentication (if service)
- **Body**:

```json
{
  "action": "string - Action type (required)",
  "data": {}
}
```

**Response**:

- **Status Code**: 200
- **Body**: (varies based on action)

**Error Responses**:

- `400 Bad Request`: Invalid payload
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Server error

**Notes**:

- Internal endpoint for batch operations
- Actions may include archiving users, updating Discord status, etc.
