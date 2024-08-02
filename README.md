# Flask RESTful API with JWT Authentication

## Setup

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables in a `.env` file:
    ```
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    DATABASE_URL=postgresql://postgres:p@stgress@localhost:5433/your_database_name
    ```

4. Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

6. Create the default admin user:
    ```bash
    python default_users.py
    ```
    

## API Endpoints

### Auth

- **Register:** `POST /auth/register`
- **Login:** `POST /auth/login`
- **Reset Password:** `POST /auth/reset_password`

### User

- **Modify User:** `PUT /user/<user_id>` (Admin only)
- **Delete User:** `DELETE /user/<user_id>` (Admin only)

### Notes

- JWT token is required for authentication. Include it in the `Authorization` header as `Bearer <JWT_TOKEN>`.
- Admin users can modify or delete non-admin users but cannot modify or delete other admin users.
