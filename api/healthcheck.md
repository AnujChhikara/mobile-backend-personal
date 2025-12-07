# Health Check API

## Overview

The Health Check API provides endpoints to check the server's health status and uptime.

## Base Path

`/healthcheck`

---

## Endpoints

### GET /

**Description**: Get server health status and uptime (public endpoint)

**Authentication**: Not required

**Request**:

- No parameters required

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "uptime": 12345.67
}
```

**Mock Response Example**:

```json
{
  "uptime": 86400.5
}
```

**Error Responses**:

- `500 Internal Server Error`: Server error

---

### GET /v2

**Description**: Get server health status and uptime (authenticated endpoint)

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "uptime": 12345.67
}
```

**Mock Response Example**:

```json
{
  "uptime": 86400.5
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error
