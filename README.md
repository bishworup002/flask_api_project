# Flask RESTful API with JWT Authentication

## Table of Contents
1. [Setup](#1-setup)
   - [Clone the Repository](#clone-the-repository)
   - [Environment Setup](#environment-setup)
   - [Database Initialization](#database-initialization)
   - [Running the Application](#running-the-application)
2. [API Endpoints](#2-api-endpoints)
   - [POST /auth/register](#post-authregister)
   - [POST /auth/login](#post-authlogin)
   - [POST /auth/reset_password](#post-authreset_password)
   - [POST /auth/forget_password](#post-authforget_password)
   - [POST /auth/reset_password/<token>](#post-authreset_passwordtoken)
   - [PUT /user/<user_id>](#put-useruser_id)
   - [DELETE /user/<user_id>](#delete-useruser_id)
3. [Notes](#3-notes)

## 1. Setup

### Clone the Repository

1. Open your terminal and navigate to the directory where you want to store the project.

2. Clone the repository:
   ```bash
   git clone https://github.com/bishworup002/flask_api_project.git
   ```

3. Navigate into the project directory:
   ```bash
   cd flask_api_project
   ```

### Environment Setup

4. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up environment variables in a `.env` file:
    ```
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    DATABASE_URL=postgresql://postgres:password@localhost:port/your_database_name
    ```

### Database Initialization

7. Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

8. Create the default  user:
    ```bash
    python default_users.py
    ```

### Running the Application

9. Run the application:
    ```bash
    flask run
    ```

### The API will be available at `http://localhost:5000`.

## 2. API Endpoints

### POST /auth/register

Register a new user.

Request:
```json
POST /auth/register
Content-Type: application/json

{
  "username": "newuser",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

Response:
```json
{
  "msg": "User created successfully"
}
```

### POST /auth/login

Authenticate a user and receive a JWT token.

Request:
```json
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "adminpassword"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### POST /auth/reset_password

Reset user's password (requires authentication).

Request:
```json
POST /auth/reset_password
Content-Type: application/json
Authorization: Bearer <your_jwt_token>

{
  "old_password": "securepassword123",
  "new_password": "evenmore_secure_password456"
}
```

Response:
```json
{
  "msg": "Password updated successfully"
}
```

### POST /auth/forget_password

Request a password reset link.

Request:
```json
POST /auth/forget_password
Content-Type: application/json

{
  "email": "john.doe@example.com"
}
```

Response:
```json
{
  "msg": "Password reset link generated successfully",
  "reset_link": "http://yourdomain.com/auth/reset_password/<token>"
}
```

### POST /auth/reset_password/<token>

Reset password using a token.

Request:
```json
POST /auth/reset_password/<token>
Content-Type: application/json

{
  "new_password": "new_secure_password789"
}
```

Response:
```json
{
  "msg": "Your password has been updated"
}
```

### PUT /user/<user_id>

Update user information (requires admin authentication).

Request:
```json
PUT /user/1
Content-Type: application/json
Authorization: Bearer <admin_jwt_token>

{
  "username": "updated_username",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "active": true,
  "role": "ADMIN"
}
```

Response:
```json
{
  "msg": "User updated successfully"
}
```

### DELETE /user/<user_id>

Delete a user (requires admin authentication).

Request:
```
DELETE /user/1
Authorization: Bearer <admin_jwt_token>
```

Response:
```json
{
  "msg": "User deleted successfully"
}
```

## 3. Notes

- JWT token is required for authentication. Include it in the `Authorization` header as `Bearer <JWT_TOKEN>`.
- Admin users can modify or delete non-admin users but cannot modify or delete other admin users.
- Make sure to replace `your-username` and `your-repo-name` in the clone URL with the actual GitHub username and repository name.

