# Expo Token Backend

A FastAPI backend for managing Expo push notification tokens with MongoDB.

## Features

- ✅ Health check endpoint
- ✅ CRUD operations for Expo tokens
- ✅ Flexible database configuration (Docker or MongoDB Atlas)
- ✅ Async MongoDB support with Motor
- ✅ Auto-generated API documentation
- ✅ **MCP (Model Context Protocol) AI Chat Interface** - Conversational task creation with LLM support

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # MongoDB connection
│   ├── models.py         # Pydantic models
│   ├── mcp_server.py     # MCP server with tools
│   ├── llm_client.py     # LLM client (Google Gemini)
│   ├── rate_limiter.py   # Rate limiting logic
│   └── routers/
│       ├── __init__.py
│       ├── health.py     # Health check routes
│       ├── expo_tokens.py # Expo token CRUD routes
│       └── ai.py         # AI chat endpoint with MCP
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

# AI Provider Configuration (Google Gemini)
GOOGLE_API_KEY=your-gemini-api-key-here

# AI Model (optional, defaults to gemini-1.5-flash)
AI_MODEL=gemini-1.5-flash

# Backend API URL (for task creation)
BACKEND_URL=https://staging-api.realdevsquad.com

# Rate Limiting
RATE_LIMIT=20  # API calls per day per user
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

### AI Chat (MCP)

| Method | Endpoint               | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| POST   | `/api/ai/chat`         | Chat interface with MCP tools      |
| POST   | `/api/ai/chat/confirm` | Confirm and execute pending action |

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

## MCP (Model Context Protocol) AI Chat Interface

The backend includes an AI-powered chat interface using MCP (Model Context Protocol) that allows users to create tasks through natural language conversation. The system uses Google Gemini as the LLM provider and includes rate limiting, session management, and confirmation flows.

### Features

- **Conversational Interface**: Natural language task creation with context retention
- **Google Gemini Integration**: Powered by Google Gemini for natural language understanding
- **MCP Tools**: Structured tool calling for task creation
- **Rate Limiting**: Per-user, per-day API call limits (configurable)
- **Session Management**: 10-minute conversation expiry with MongoDB storage
- **Confirmation Flow**: User confirmation required before executing actions
- **Typos & Variations**: Handles common typos and natural language variations

### Setup

1. **Configure Google Gemini**

   Add to your `.env` file:

   ```env
   # Google Gemini API Key
   GOOGLE_API_KEY=your-gemini-key-here
   
   # Optional: Choose Gemini model (default: gemini-1.5-flash)
   AI_MODEL=gemini-1.5-flash
   ```

2. **Configure Backend API**

   ```env
   BACKEND_URL=https://staging-api.realdevsquad.com
   ```

3. **Set Rate Limit** (optional, default: 20)

   ```env
   RATE_LIMIT=20  # API calls per day per user
   ```

### API Usage

#### Start a Chat Conversation

```bash
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-auth-token" \
  -d '{
    "message": "creat a task with title Fix bug and deadline dec 25 2026",
    "user_id": "user123"
  }'
```

**Response:**

```json
{
  "message": "I'll create a task 'Fix bug' with deadline December 25, 2026. Should I proceed? (yes/no)",
  "session_id": "uuid-session-id",
  "requires_confirmation": true,
  "pending_action": {
    "action": "createTask",
    "data": {
      "title": "Fix bug",
      "endsOn": 1735084800
    }
  },
  "success": true
}
```

#### Confirm Action

```bash
curl -X POST "http://localhost:8000/api/ai/chat/confirm?session_id=uuid-session-id&confirmed=true&user_id=user123" \
  -H "Authorization: Bearer your-auth-token"
```

**Response:**

```json
{
  "message": "✅ Task created successfully!",
  "session_id": "uuid-session-id",
  "requires_confirmation": false,
  "pending_action": null,
  "success": true
}
```

#### Continue Conversation

Use the `session_id` from the first response to continue the conversation:

```bash
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-auth-token" \
  -d '{
    "message": "what tasks did I create?",
    "user_id": "user123",
    "session_id": "uuid-session-id"
  }'
```

### MCP Tools

#### createTask

Creates a new task with the following parameters:

- **Required**: `title` (string)
- **Optional**:
  - `description` (string)
  - `endsOn` (number) - Unix timestamp in seconds
  - `priority` (string) - One of: "LOW", "MEDIUM", "HIGH", "URGENT"
  - `assignee` (string) - User ID of assignee
  - `type` (string) - Task type

**Example User Inputs:**

- "creat a task with title Fix bug" (handles typos)
- "create task Fix bug with deadline dec 25 2026"
- "make a task called Fix bug high priority"
- "add task Fix bug assign to user456"

### Conversation Flow

1. **User sends message** → `/api/ai/chat`
2. **LLM analyzes** → Extracts intent and data
3. **Validation** → Checks required fields, deadlines, etc.
4. **Confirmation request** → Returns confirmation message with `session_id`
5. **User confirms** → `/api/ai/chat/confirm` with `confirmed=true`
6. **Action executed** → Calls backend API and returns result

### Rate Limiting

- **Limit**: Configurable via `RATE_LIMIT` env var (default: 20)
- **Scope**: Per-user, per-day
- **Reset**: Daily at 00:00:00 UTC
- **Error**: Returns `429 Too Many Requests` when exceeded

### Session Management

- **Expiry**: 10 minutes from last message
- **Storage**: MongoDB `conversations` collection
- **Context**: Full conversation history maintained
- **Token**: Auth token stored in session for backend API calls

### Error Handling

- **Rate Limit Exceeded**: `429` with reset time
- **Session Expired**: `410 Gone` - start new conversation
- **Invalid Input**: LLM asks for clarification
- **Backend API Error**: Returns error message to user

### Example Conversation

```
User: "creat a task fix bug"
Assistant: "I can help you create a task. What should the task title be?"

User: "Fix critical bug in login"
Assistant: "I'll create a task 'Fix critical bug in login'. Should I proceed? (yes/no)"

User: "yes"
Assistant: "✅ Task created successfully!"
```

### Database Collections

#### conversations

Stores chat conversations with nested messages:

```javascript
{
  "user_id": "user123",
  "session_id": "uuid",
  "token": "auth-token",
  "status": "active",
  "messages": [
    {
      "role": "user",
      "content": "creat task",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "I'll create...",
      "timestamp": "2024-01-15T10:00:05Z",
      "requires_confirmation": true,
      "pending_action": {...}
    }
  ],
  "expires_at": "2024-01-15T10:10:00Z"
}
```

#### rate_limits

Tracks daily API call counts per user:

```javascript
{
  "user_id": "user123",
  "date": "2024-01-15",
  "count": 5,
  "limit": 20,
  "next_reset": "2024-01-16T00:00:00Z"
}
```

### Mobile App Integration

```javascript
// Step 1: Start conversation
const response = await fetch("/api/ai/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    message: "creat a task fix bug",
    user_id: "user123",
  }),
});

const data = await response.json();
// Store session_id: data.session_id

// Step 2: If confirmation required, show dialog
if (data.requires_confirmation) {
  // Show: data.message
  // User clicks "Yes" or "No"

  // Step 3: Confirm
  const confirmResponse = await fetch(
    `/api/ai/chat/confirm?session_id=${data.session_id}&confirmed=true&user_id=user123`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
}
```

### Troubleshooting

**Issue**: "OpenAI API key not configured"

- **Solution**: Set `OPENAI_API_KEY` in `.env` (or corresponding key for your provider)

**Issue**: "Rate limit exceeded"

- **Solution**: Wait until next day (00:00 UTC) or increase `RATE_LIMIT` in `.env`

**Issue**: "Session expired"

- **Solution**: Start a new conversation (don't send `session_id`)

**Issue**: LLM not understanding request

- **Solution**: Be more specific, include required fields (e.g., "create task with title X")

## Switching Between Docker and Atlas

Simply change the `DB_MODE` in your `.env` file:

```env
# For Docker (local)
DB_MODE=docker

# For Atlas (cloud)
DB_MODE=atlas
```

Then restart the server.

## Development

### Code Quality with Ruff

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

#### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

#### Lint Code

```bash
# Check for linting issues
ruff check .

# Auto-fix linting issues
ruff check --fix .
```

#### Format Code

```bash
# Check formatting
ruff format --check .

# Format code
ruff format .
```

#### Run Both (Lint + Format)

```bash
# Check everything
ruff check . && ruff format --check .

# Fix everything
ruff check --fix . && ruff format .
```

#### Pre-commit (Optional)

You can add Ruff to your git workflow:

```bash
# Before committing, run:
ruff check --fix . && ruff format .
```

Or set up a pre-commit hook (see `.git/hooks/pre-commit`).

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
