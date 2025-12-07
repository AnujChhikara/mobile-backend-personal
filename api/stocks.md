# Stocks API

## Overview

The Stocks API provides endpoints for managing stocks in the system. Stocks represent tradeable items with quantity and price.

## Base Path

`/stocks`

---

## Endpoints

### GET /

**Description**: Get all stocks in the system

**Authentication**: Not required

**Request**:

- No parameters required

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Stocks returned successfully!" | "No stocks found",
  "stock": [
    {
      "id": "string - Stock ID",
      "name": "string - Stock name",
      "quantity": "number - Available quantity",
      "price": "number - Stock price",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ]
}
```

**Mock Response Example** (with stocks):

```json
{
  "message": "Stocks returned successfully!",
  "stock": [
    {
      "id": "stock1",
      "name": "RDS Coin",
      "quantity": 1000,
      "price": 10.5,
      "createdAt": "2024-01-15T10:00:00Z",
      "updatedAt": "2024-01-15T10:00:00Z"
    },
    {
      "id": "stock2",
      "name": "Dev Token",
      "quantity": 500,
      "price": 25.0,
      "createdAt": "2024-01-15T10:05:00Z",
      "updatedAt": "2024-01-15T10:05:00Z"
    }
  ]
}
```

**Mock Response Example** (no stocks):

```json
{
  "message": "No stocks found",
  "stock": []
}
```

**Error Responses**:

- `500 Internal Server Error`: Server error

---

### POST /

**Description**: Create a new stock

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "name": "string - Stock name (required)",
  "quantity": "number - Initial quantity (required)",
  "price": "number - Stock price (required)"
}
```

**Mock Request Example**:

```json
{
  "name": "RDS Coin",
  "quantity": 1000,
  "price": 10.5
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Stock created successfully!",
  "stock": {
    "name": "string - Stock name",
    "quantity": "number - Quantity",
    "price": "number - Price",
    "createdAt": "timestamp",
    "updatedAt": "timestamp"
  },
  "id": "string - Stock ID"
}
```

**Mock Response Example**:

```json
{
  "message": "Stock created successfully!",
  "stock": {
    "name": "RDS Coin",
    "quantity": 1000,
    "price": 10.5,
    "createdAt": "2024-01-15T10:00:00Z",
    "updatedAt": "2024-01-15T10:00:00Z"
  },
  "id": "stock1"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### GET /user/self

**Description**: Get stocks owned by the authenticated user

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}

**Response**:

- **Status Code**: 200
- **Headers**:
  - `X-Deprecation-Warning`: Warning about endpoint deprecation
- **Body**:

```json
{
  "message": "User stocks returned successfully!" | "No stocks found",
  "userStocks": [
    {
      "stockId": "string - Stock ID",
      "stockName": "string - Stock name",
      "quantity": "number - User's quantity",
      "price": "number - Current price"
    }
  ]
}
```

**Mock Response Example** (with stocks):

```json
{
  "message": "User stocks returned successfully!",
  "userStocks": [
    {
      "stockId": "stock1",
      "stockName": "RDS Coin",
      "quantity": 50,
      "price": 10.5
    }
  ]
}
```

**Mock Response Example** (no stocks):

```json
{
  "message": "No stocks found",
  "userStocks": []
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error

**Notes**:

- This endpoint is deprecated. Use `/stocks/:userId` instead.

---

### GET /:userId

**Description**: Get stocks owned by a specific user

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `userId`: string - The ID of the user whose stocks to retrieve

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "User stocks returned successfully!" | "No stocks found",
  "userStocks": [
    {
      "stockId": "string - Stock ID",
      "stockName": "string - Stock name",
      "quantity": "number - User's quantity",
      "price": "number - Current price"
    }
  ]
}
```

**Mock Request Example**:

- Path: `/stocks/user789`

**Mock Response Example**:

```json
{
  "message": "User stocks returned successfully!",
  "userStocks": [
    {
      "stockId": "stock1",
      "stockName": "RDS Coin",
      "quantity": 50,
      "price": 10.5
    },
    {
      "stockId": "stock2",
      "stockName": "Dev Token",
      "quantity": 20,
      "price": 25.0
    }
  ]
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (user can only access their own stocks unless authorized)
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server error
