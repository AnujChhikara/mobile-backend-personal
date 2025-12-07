# Items API

## Overview

The Items API provides endpoints for managing items and their associated tags and levels. Items can be filtered based on various criteria.

## Base Path

`/items`

---

## Endpoints

### POST /

**Description**: Add tags to an item with corresponding levels

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "itemId": "string - Item ID (required, trimmed)",
  "itemType": "string - Item type (required, must be one of valid types, will be uppercased)",
  "tagPayload": [
    {
      "tagId": "string - Tag ID (required)",
      "levelId": "string - Level ID (required)"
    }
  ]
}
```

**Mock Request Example**:

```json
{
  "itemId": "item123",
  "itemType": "task",
  "tagPayload": [
    {
      "tagId": "tag123",
      "levelId": "level2"
    },
    {
      "tagId": "tag124",
      "levelId": "level1"
    }
  ]
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Tags added successfully!",
  "itemId": "string - Item ID"
}
```

**Mock Response Example**:

```json
{
  "message": "Tags added successfully!",
  "itemId": "item123"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields or invalid type)
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `500 Internal Server Error`: Server error

---

### DELETE /

**Description**: Remove tags from an item

**Authentication**: Required - SUPERUSER role

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Body**:

```json
{
  "itemId": "string - Item ID",
  "tagId": "string - Tag ID to remove"
}
```

**Mock Request Example**:

```json
{
  "itemId": "item123",
  "tagId": "tag123"
}
```

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Tags removed successfully!",
  "itemId": "string - Item ID",
  "tagId": "string - Removed tag ID"
}
```

**Mock Response Example**:

```json
{
  "message": "Tags removed successfully!",
  "itemId": "item123",
  "tagId": "tag123"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions (not SUPERUSER)
- `404 Not Found`: Item or tag not found
- `500 Internal Server Error`: Server error

---

### GET /filter

**Description**: Get items based on filter criteria

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Query Parameters** (at least one required):
  - `itemType`: string (optional) - Filter by item type (uppercase)
  - `itemId`: string (optional) - Filter by specific item ID
  - `levelId`: string (optional) - Filter by level ID
  - `levelName`: string (optional) - Filter by level name
  - `levelNumber`: number (optional) - Filter by level number
  - `tagId`: string (optional) - Filter by tag ID
  - `tagType`: string (optional) - Filter by tag type (uppercase)

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Items fetched Successfully",
  "data": [
    {
      "itemId": "string - Item ID",
      "itemType": "string - Item type",
      "tags": [
        {
          "tagId": "string - Tag ID",
          "tagName": "string - Tag name",
          "levelId": "string - Level ID",
          "levelName": "string - Level name",
          "levelValue": "number - Level value"
        }
      ]
    }
  ]
}
```

**Mock Request Example**:

- Path: `/items/filter?itemType=TASK&tagId=tag123`

**Mock Response Example**:

```json
{
  "message": "Items fetched Successfully",
  "data": [
    {
      "itemId": "item123",
      "itemType": "TASK",
      "tags": [
        {
          "tagId": "tag123",
          "tagName": "JavaScript",
          "levelId": "level2",
          "levelName": "Intermediate",
          "levelValue": 2
        }
      ]
    }
  ]
}
```

**Error Responses**:

- `400 Bad Request`: No filter provided or invalid query parameters
- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: Server error
