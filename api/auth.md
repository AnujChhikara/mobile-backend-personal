# Authentication API

## Overview

The Authentication API provides endpoints for user authentication via GitHub and Google OAuth, QR code authentication for mobile devices, and session management.

## Base Path

`/auth`

---

## Endpoints

### GET /github/login

**Description**: Initiate GitHub OAuth login flow. Redirects to GitHub for authentication.

**Authentication**: Not required

**Request**:

- **Query Parameters**:
  - `redirectURL`: string (optional) - URL to redirect to after authentication
  - `sourceUtm`: string (optional) - Source identifier (e.g., "rds-mobile-app")

**Response**:

- **Status Code**: 302 (Redirect to GitHub)
- Redirects to GitHub OAuth authorization page

**Notes**:

- After GitHub authentication, user is redirected to `/auth/github/callback`
- For mobile apps (sourceUtm=rds-mobile-app), the redirectURL is modified to include `isMobileApp=true`
- Developers must use GitHub login (Google login is restricted for developers)

---

### GET /github/callback

**Description**: GitHub OAuth callback handler. Processes authentication and sets session cookie.

**Authentication**: Not required (handled by OAuth flow)

**Request**:

- This endpoint is called by GitHub OAuth provider
- Query parameters are set by GitHub during OAuth flow

**Response**:

- **Status Code**: 302 (Redirect)
- Sets authentication cookie: `rds-session-{env}`
- Optionally sets `rds-session-v2-{env}` cookie if `v2=true` in redirect URL
- Redirects to:
  - Original redirectURL (if valid and from realdevsquad.com domain)
  - `https://my.realdevsquad.com/new-signup` (if user has incomplete profile)
  - Default RDS UI URL

**Mock Response Flow**:

1. User authenticates with GitHub
2. GitHub redirects to `/auth/github/callback?code=...&state=...`
3. Server processes authentication
4. Sets session cookie
5. Redirects to specified URL

**Error Responses**:

- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: GitHub login restricted (non-developers must use Google login)

**Notes**:

- Only users with DEVELOPER role can use GitHub login
- Non-developers are redirected with error message to use Google login
- Mobile app users receive token in redirect URL query parameter

---

### GET /google/login

**Description**: Initiate Google OAuth login flow. Redirects to Google for authentication. (Dev flag required)

**Authentication**: Not required (dev flag middleware required)

**Request**:

- **Query Parameters**:
  - `redirectURL`: string (optional) - URL to redirect to after authentication

**Response**:

- **Status Code**: 302 (Redirect to Google)
- Redirects to Google OAuth authorization page

**Notes**:

- This endpoint requires dev flag to be enabled
- After Google authentication, user is redirected to `/auth/google/callback`
- Developers cannot use Google login (must use GitHub)

---

### GET /google/callback

**Description**: Google OAuth callback handler. Processes authentication and sets session cookie.

**Authentication**: Not required (handled by OAuth flow)

**Request**:

- This endpoint is called by Google OAuth provider
- Query parameters are set by Google during OAuth flow

**Response**:

- **Status Code**: 302 (Redirect)
- Sets authentication cookie: `rds-session-{env}`
- Redirects to:
  - Original redirectURL (if valid and from realdevsquad.com domain)
  - `https://my.realdevsquad.com/new-signup` (if user has incomplete profile)
  - Default RDS UI URL

**Error Responses**:

- `401 Unauthorized`: No email found or no verified email in Google account
- `403 Forbidden`: Google login restricted for developers (must use GitHub)

**Notes**:

- Developers cannot use Google login (must use GitHub login)
- Requires verified email in Google account

---

### GET /signout

**Description**: Sign out the current user by clearing authentication cookies

**Authentication**: Not required

**Request**:

- No parameters required

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Signout successful"
}
```

**Mock Response Example**:

```json
{
  "message": "Signout successful"
}
```

**Notes**:

- Clears both `rds-session-{env}` and `rds-session-v2-{env}` cookies

---

### GET /qr-code-auth

**Description**: Fetch user device information for QR code authentication

**Authentication**: Not required

**Request**:

- **Query Parameters**:
  - `device_id`: string (required) - Device ID to look up

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Authentication document retrieved successfully.",
  "data": {
    "user_id": "string - User ID",
    "device_id": "string - Device ID",
    "device_info": "string - Device information",
    "authorization_status": "string - Status: NOT_INIT, AUTHORIZED, or REJECTED"
  }
}
```

**Mock Request Example**:

- Path: `/auth/qr-code-auth?device_id=device123`

**Mock Response Example**:

```json
{
  "message": "Authentication document retrieved successfully.",
  "data": {
    "user_id": "user123",
    "device_id": "device123",
    "device_info": "iPhone 13, iOS 16.0",
    "authorization_status": "NOT_INIT"
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid query parameters (device_id missing)
- `404 Not Found`: User with the device_id does not exist
- `500 Internal Server Error`: Server error

---

### POST /qr-code-auth

**Description**: Store user device information for QR code authentication

**Authentication**: Not required

**Request**:

- **Body**:

```json
{
  "user_id": "string - User ID (required)",
  "device_info": "string - Device information string (required)",
  "device_id": "string - Device ID (required)"
}
```

**Mock Request Example**:

```json
{
  "user_id": "user123",
  "device_info": "iPhone 13, iOS 16.0",
  "device_id": "device123"
}
```

**Response**:

- **Status Code**: 201
- **Body**:

```json
{
  "message": "Data added successfully",
  "user_id": "string - User ID",
  "device_id": "string - Device ID",
  "device_info": "string - Device information",
  "authorization_status": "NOT_INIT"
}
```

**Mock Response Example**:

```json
{
  "message": "Data added successfully",
  "user_id": "user123",
  "device_id": "device123",
  "device_info": "iPhone 13, iOS 16.0",
  "authorization_status": "NOT_INIT"
}
```

**Error Responses**:

- `400 Bad Request`: Invalid payload (missing required fields)
- `404 Not Found`: User does not exist
- `500 Internal Server Error`: Server error

---

### GET /device

**Description**: Get device details for the authenticated user

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Authentication document Exists",
  "data": {
    "device_info": "string - Device information"
  }
}
```

**Mock Response Example**:

```json
{
  "message": "Authentication document Exists",
  "data": {
    "device_info": "iPhone 13, iOS 16.0"
  }
}
```

**Error Responses**:

- `401 Unauthorized`: Not authenticated
- `404 Not Found`: User device information not found
- `500 Internal Server Error`: Server error

---

### PATCH /qr-code-auth/authorization_status/:authorization_status

**Description**: Update the authorization status for QR code authentication

**Authentication**: Required

**Request**:

- **Headers**:
  - `Cookie`: rds-session-{env}
- **Path Parameters**:
  - `authorization_status`: string (required) - Must be one of: "AUTHORIZED", "REJECTED", "NOT_INIT"

**Response**:

- **Status Code**: 200
- **Body**:

```json
{
  "message": "Authentication document for user {userId} updated successfully",
  "data": {
    "user_id": "string - User ID",
    "device_id": "string - Device ID",
    "device_info": "string - Device information",
    "authorization_status": "string - Updated status",
    "token": "string - Auth token (if status is AUTHORIZED)"
  }
}
```

**Mock Request Example**:

- Path: `/auth/qr-code-auth/authorization_status/AUTHORIZED`

**Mock Response Example**:

```json
{
  "message": "Authentication document for user user123 updated successfully",
  "data": {
    "user_id": "user123",
    "device_id": "device123",
    "device_info": "iPhone 13, iOS 16.0",
    "authorization_status": "AUTHORIZED",
    "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses**:

- `400 Bad Request`: Invalid authorization_status parameter
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Authentication document not found
- `500 Internal Server Error`: Server error

**Notes**:

- If status is set to "AUTHORIZED", an authentication token is generated and included in the response
- The token can be used for subsequent authenticated requests
