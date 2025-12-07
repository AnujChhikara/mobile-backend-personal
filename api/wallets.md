# Wallets API

## Overview

The Wallets API provides endpoints for managing user wallets. Wallets track user currency/points balance and transactions.

## Base Path

`/wallet`

---

## Endpoints

### GET /

**Description**: Get the authenticated user's wallet. Creates a default wallet if one doesn't exist.

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Wallet returned successfully for user",
  "wallet": {
    "id": "string - Wallet ID",
    "userId": "string - User ID",
    "amount": "number - Current balance",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Wallet returned successfully for user",
  "wallet": {
    "id": "wallet123",
    "userId": "user123",
    "amount": 1000,
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error

**Notes**:

- If the user doesn't have a wallet, a default wallet is automatically created with initial balance

---

### GET /:username

**Description**: Get a specific user's wallet by username. Only accessible by SUPERUSERs.

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `username`: string - Username of the user

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Wallet returned successfully",
  "wallet": {
    "id": "string - Wallet ID",
    "userId": "string - User ID",
    "amount": "number - Current balance",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  }
}
```

**Mock Request Example**:

- Path: `/wallet/johndoe`

**Mock Response Example**:

```json
{
  "message": "Wallet returned successfully",
  "wallet": {
    "id": "wallet456",
    "userId": "user456",
    "amount": 500,
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  }
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server error

**Notes**:

- If the user doesn't have a wallet, a default wallet is automatically created with initial balance
