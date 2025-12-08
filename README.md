# Expo Tokens API

A Bun-based REST API server for managing Expo push notification tokens with MongoDB integration.

## Prerequisites

- [Bun](https://bun.sh) installed (v1.3.4 or later)
- [Docker](https://www.docker.com/) and Docker Compose (for local MongoDB) OR MongoDB Atlas account

## Installation

```bash
bun install
```

## Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` with your database configuration:

### Database Configuration

Set `DB_MODE` to either `"docker"` for local MongoDB or `"atlas"` for MongoDB Atlas.

#### Docker Mode (Local MongoDB)

1. Start MongoDB using Docker Compose:

```bash
docker-compose up -d
```

2. Configure your `.env` file:

```env
DB_MODE=docker
MONGO_DOCKER_HOST=localhost
MONGO_DOCKER_PORT=27017
MONGO_DOCKER_USER=admin
MONGO_DOCKER_PASSWORD=password123
DATABASE_NAME=expo_tokens_db
```

To stop MongoDB:

```bash
docker-compose down
```

To stop and remove volumes (deletes all data):

```bash
docker-compose down -v
```

#### Atlas Mode (MongoDB Atlas)

```env
DB_MODE=atlas
MONGO_ATLAS_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=expo_tokens_db
```

### Server Configuration

```env
PORT=8000
```

## Running the Server

Development mode (with hot reload):

```bash
bun run dev
```

Production mode:

```bash
bun run start
```

The server will start on `http://localhost:8000` (or the port specified in your `.env` file).

## API Endpoints

### Health Check

| Method | Endpoint  | Description  |
| ------ | --------- | ------------ |
| GET    | `/health` | Health check |

### Expo Tokens

| Method | Endpoint                          | Description               |
| ------ | --------------------------------- | ------------------------- |
| POST   | `/api/expo-tokens/`               | Create/Update expo token  |
| GET    | `/api/expo-tokens/`               | Get all expo tokens       |
| GET    | `/api/expo-tokens/{id}`           | Get expo token by ID      |
| GET    | `/api/expo-tokens/user/{user_id}` | Get expo token by user ID |
| PUT    | `/api/expo-tokens/{id}`           | Update expo token         |
| DELETE | `/api/expo-tokens/{id}`           | Delete expo token by ID   |
| DELETE | `/api/expo-tokens/user/{user_id}` | Delete expo token by user |

## API Examples

### Create/Update Expo Token

```bash
curl -X POST "http://localhost:8000/api/expo-tokens/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "expo_token": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
  }'
```

### Get All Expo Tokens

```bash
curl "http://localhost:8000/api/expo-tokens/"
```

### Get Expo Token by ID

```bash
curl "http://localhost:8000/api/expo-tokens/{id}"
```

### Get Expo Token by User ID

```bash
curl "http://localhost:8000/api/expo-tokens/user/user123"
```

### Update Expo Token

```bash
curl -X PUT "http://localhost:8000/api/expo-tokens/{id}" \
  -H "Content-Type: application/json" \
  -d '{
    "expo_token": "ExponentPushToken[yyyyyyyyyyyyyyyyyyyyyy]"
  }'
```

### Delete Expo Token by ID

```bash
curl -X DELETE "http://localhost:8000/api/expo-tokens/{id}"
```

### Delete Expo Token by User ID

```bash
curl -X DELETE "http://localhost:8000/api/expo-tokens/user/user123"
```

## Response Format

All responses are in JSON format:

### Success Response

```json
{
  "_id": "...",
  "user_id": "user123",
  "expo_token": "ExponentPushToken[...]",
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

### Error Response

```json
{
  "error": "Error message"
}
```

## Project Structure

```
/
├── .env.example          # Environment variables template
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── index.ts              # Main server file
├── src/
│   ├── db/
│   │   └── connection.ts    # MongoDB connection utility
│   ├── models/
│   │   └── expoToken.ts      # ExpoToken model and collection helper
│   └── routes/
│       └── expoTokens.ts     # Expo tokens API routes
└── README.md
```

## Notes

- The POST endpoint implements upsert logic: if a token exists for the given `user_id`, it will be updated; otherwise, a new token will be created.
- Bun automatically loads `.env` files, so no additional configuration is needed.
- The server uses `Bun.serve()` for routing and request handling.
