# API Documentation

This directory contains comprehensive API documentation for all modules in the website-backend.

## Table of Contents

### Core Modules

- [Health Check](./healthcheck.md) - Server health status endpoints
- [Authentication](./auth.md) - User authentication and authorization

### User Management

- [Users](./users.md) - User profile and management
- [User Status](./userStatus.md) - User status tracking
- [Profile Diffs](./profileDiffs.md) - Profile change tracking
- [External Accounts](./external-accounts.md) - External account management

### Content & Features

- [Questions](./questions.md) - Questions management
- [Answers](./answers.md) - Answers management
- [Tasks](./tasks.md) - Task management
- [Task Requests](./taskRequests.md) - Task request handling
- [Contributions](./contributions.md) - User contributions tracking
- [Pull Requests](./pullrequests.md) - Pull request management
- [Issues](./issues.md) - Issue tracking
- [Progresses](./progresses.md) - Progress tracking
- [Applications](./applications.md) - Application management

### Gamification & Rewards

- [Badges](./badges.md) - Badge management
- [Levels](./levels.md) - Level system
- [Tags](./tags.md) - Tag management
- [Items](./items.md) - Item management
- [Stocks](./stocks.md) - Stock trading system
- [Trading](./trading.md) - Trading operations
- [Wallets](./wallets.md) - User wallet management

### Events & Activities

- [Events](./events.md) - Event management
- [Arts](./arts.md) - Arts management
- [Auctions](./auctions.md) - Auction system
- [Challenges](./challenges.md) - Challenge management

### Notifications & Communication

- [Notifications](./notifications.md) - Notification system
- [FCM Tokens](./fcm-tokens.md) - Firebase Cloud Messaging tokens
- [Invites](./invites.md) - Invitation management
- [Requests](./requests.md) - Request management

### Integrations

- [Discord Actions](./discord-actions.md) - Discord integration
- [Extension Requests](./extensionRequests.md) - Extension request management

### Admin & Utilities

- [AWS Access](./awsAccess.md) - AWS group management
- [Cloudflare Cache](./cloudflareCache.md) - Cache management
- [Logs](./logs.md) - Log management
- [Monitor](./monitor.md) - Progress monitoring
- [Staging](./staging.md) - Staging environment utilities
- [Impersonation](./impersonation.md) - User impersonation (dev only)
- [Subscription](./subscription.md) - Subscription management
- [Goals](./goals.md) - Goals management

## Common Patterns

### Authentication

Most endpoints require authentication via session cookie:

- Cookie name: `rds-session-{env}` (e.g., `rds-session-development`)
- Cookie is set automatically after successful authentication

### Authorization

Endpoints may require specific roles:

- `SUPERUSER` - Full administrative access
- `APPOWNER` - Application owner privileges
- `MEMBER` - Regular member access
- `DEVELOPER` - Developer role

### Error Responses

All endpoints follow a consistent error response format:

- `400 Bad Request` - Invalid request payload or parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Response Format

Successful responses typically follow this structure:

```json
{
  "message": "Success message",
  "data": {}
}
```

## Base URL

- Development: `http://localhost:3000`
- Production: `https://api.realdevsquad.com`
