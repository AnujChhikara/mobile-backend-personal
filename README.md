# Expo Token Backend

A FastAPI backend for managing Expo push notification tokens with MongoDB.

## Features

- ✅ Health check endpoint
- ✅ CRUD operations for Expo tokens
- ✅ Flexible database configuration (Docker or MongoDB Atlas)
- ✅ Async MongoDB support with Motor
- ✅ Auto-generated API documentation

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # MongoDB connection
│   ├── models.py         # Pydantic models
│   └── routers/
│       ├── __init__.py
│       ├── health.py     # Health check routes
│       └── expo_tokens.py # Expo token CRUD routes
├── docker-compose.yml    # Docker setup for MongoDB
├── requirements.txt      # Python dependencies
├── run.py               # Entry point
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Database Configuration
# Set to "docker" for local MongoDB, or "atlas" for MongoDB Atlas
DB_MODE=docker

# Docker MongoDB Settings (used when DB_MODE=docker)
MONGO_DOCKER_HOST=localhost
MONGO_DOCKER_PORT=27017
MONGO_DOCKER_USER=admin
MONGO_DOCKER_PASSWORD=password123

# MongoDB Atlas Settings (used when DB_MODE=atlas)
MONGO_ATLAS_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Database Name
DATABASE_NAME=expo_tokens_db

# Scheduler/Cron Settings
# Set to "true" to enable scheduled tasks, "false" to disable
RUN_CRON=true
```

### 3. Choose Your Database Option

#### Option A: Docker MongoDB (Local Development)

```bash
# Start MongoDB with Docker
docker-compose up -d

# Verify MongoDB is running
docker ps
```

MongoDB will be available at `localhost:27017`  
Mongo Express GUI at `http://localhost:8081`

#### Option B: MongoDB Atlas (Cloud)

1. Create a cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Get your connection string
3. Update `.env`:
   ```env
   DB_MODE=atlas
   MONGO_ATLAS_URI=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/
   ```

### 4. Run the Server

```bash
python run.py
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be running at `http://localhost:8000`

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health

| Method | Endpoint  | Description  |
| ------ | --------- | ------------ |
| GET    | `/`       | Service info |
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

## Example Requests

### Create Expo Token

```bash
curl -X POST "http://localhost:8000/api/expo-tokens/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "expo_token": "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
  }'
```

### Get All Tokens

```bash
curl "http://localhost:8000/api/expo-tokens/"
```

### Get Token by User ID

```bash
curl "http://localhost:8000/api/expo-tokens/user/user123"
```

### Health Check

```bash
curl "http://localhost:8000/health"
```

## Switching Between Docker and Atlas

Simply change the `DB_MODE` in your `.env` file:

```env
# For Docker (local)
DB_MODE=docker

# For Atlas (cloud)
DB_MODE=atlas
```

Then restart the server.

## Docker Commands

```bash
# Start MongoDB
docker-compose up -d

# Stop MongoDB
docker-compose down

# Stop and remove volumes (deletes data)
docker-compose down -v

# View logs
docker-compose logs -f mongodb
```

## Data Model

### Expo Token

| Field      | Type     | Description                       |
| ---------- | -------- | --------------------------------- |
| id         | string   | Unique document ID (MongoDB \_id) |
| user_id    | string   | Unique user identifier            |
| expo_token | string   | Expo push notification token      |
| created_at | datetime | Creation timestamp                |
| updated_at | datetime | Last update timestamp             |
