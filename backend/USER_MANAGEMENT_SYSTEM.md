# User Management System Documentation

## Overview
This is a complete user management system with user registration, login, profile management, and password change functionality.

## Database Schema

### Users Table
The `users` table stores all user information with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key, auto-incremented |
| name | String(255) | User's full name |
| email | String(255) | User's email (unique, indexed) |
| password | String(255) | Hashed password |
| age | Integer | User's age (nullable) |
| role | Enum | User role (admin, user, moderator) |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |

## User Roles
- **ADMIN**: Full administrative access
- **USER**: Regular user (default role)
- **MODERATOR**: Moderation privileges

## API Endpoints

### 1. User Registration
**Endpoint:** `POST /users/register`

**Description:** Register a new user

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "age": 25,
  "role": "user"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 25,
  "role": "user",
  "created_at": "2025-12-09T10:30:00",
  "updated_at": "2025-12-09T10:30:00"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "age": 25,
    "role": "user"
  }'
```

---

### 2. User Login
**Endpoint:** `POST /users/login`

**Description:** Authenticate user and receive JWT tokens

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "role": "user",
    "created_at": "2025-12-09T10:30:00",
    "updated_at": "2025-12-09T10:30:00"
  }
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

---

### 3. Get User by ID
**Endpoint:** `GET /users/users/{user_id}`

**Description:** Retrieve user details by ID

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 25,
  "role": "user",
  "created_at": "2025-12-09T10:30:00",
  "updated_at": "2025-12-09T10:30:00"
}
```

**cURL:**
```bash
curl -X GET http://localhost:8000/users/users/1
```

---

### 4. List All Users
**Endpoint:** `GET /users/users`

**Description:** Get all users with pagination

**Query Parameters:**
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=10, max=100): Number of records to return

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "role": "user",
    "created_at": "2025-12-09T10:30:00",
    "updated_at": "2025-12-09T10:30:00"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 28,
    "role": "admin",
    "created_at": "2025-12-09T11:00:00",
    "updated_at": "2025-12-09T11:00:00"
  }
]
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/users/users?skip=0&limit=10"
```

---

### 5. Get Users by Role
**Endpoint:** `GET /users/users/role/{role}`

**Description:** Filter users by their role

**Path Parameters:**
- `role` (enum): admin, user, or moderator

**Query Parameters:**
- `skip` (int, default=0): Number of records to skip
- `limit` (int, default=10): Number of records to return

**cURL:**
```bash
curl -X GET "http://localhost:8000/users/users/role/admin?skip=0&limit=10"
```

---

### 6. Update User
**Endpoint:** `PUT /users/users/{user_id}`

**Description:** Update user details

**Request Body (all fields optional):**
```json
{
  "name": "John Updated",
  "email": "john.updated@example.com",
  "age": 26,
  "role": "moderator"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Updated",
  "email": "john.updated@example.com",
  "age": 26,
  "role": "moderator",
  "created_at": "2025-12-09T10:30:00",
  "updated_at": "2025-12-09T12:00:00"
}
```

**cURL:**
```bash
curl -X PUT http://localhost:8000/users/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "age": 26
  }'
```

---

### 7. Delete User
**Endpoint:** `DELETE /users/users/{user_id}`

**Description:** Delete a user account

**Response:** 204 No Content

**cURL:**
```bash
curl -X DELETE http://localhost:8000/users/users/1
```

---

### 8. Change Password
**Endpoint:** `POST /users/users/{user_id}/change-password`

**Description:** Change user password (requires old password verification)

**Request Body:**
```json
{
  "old_password": "password123",
  "new_password": "newpassword456"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "age": 25,
  "role": "user",
  "created_at": "2025-12-09T10:30:00",
  "updated_at": "2025-12-09T12:15:00"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/users/users/1/change-password \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "password123",
    "new_password": "newpassword456"
  }'
```

---

### 9. Get Total User Count
**Endpoint:** `GET /users/stats/total-users`

**Description:** Get total number of users in the system

**Response:**
```json
{
  "total_users": 42
}
```

**cURL:**
```bash
curl -X GET http://localhost:8000/users/stats/total-users
```

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file in the backend directory with the following content:
```
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=heybuddy
JWT_SECRET=your_jwt_secret_key
```

### 3. Create Database
```bash
createdb heybuddy
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. API Documentation
Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Security Features

- **Password Hashing**: Passwords are securely hashed using bcrypt
- **JWT Tokens**: Authentication via JWT tokens for stateless API
- **Email Validation**: Email format validation using Pydantic EmailStr
- **Password Requirements**: Minimum 8 characters for security
- **Email Uniqueness**: Prevents duplicate email registration
- **Age Validation**: Age must be between 0-150

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful GET request
- `201 Created`: Successful resource creation
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication failed
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Database Files Created

- `app/models.py`: SQLAlchemy User model
- `app/db.py`: Database configuration and session management
- `app/schemas.py`: Pydantic schemas for request/response validation
- `app/services/user_service.py`: Business logic for user operations
- `app/controllers/user_controller.py`: API route handlers
- `app/core/config.py`: Configuration management
- `app/core/security.py`: Password hashing and token validation

## Next Steps

The user management system is now ready to use. You can:
1. Register new users
2. Login and receive JWT tokens
3. Update user profiles
4. Manage user roles
5. Change passwords securely
6. Query users with various filters
