
# API Documentation for User and Friends Management

## 1. **User Signup API**
- **Endpoint**: `/api/signup/`
- **Method**: `POST`
- **Description**: Registers a new user.
- **Request Body (JSON)**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "strong_password"
  }
  ```
- **Response**:
  - **Success** (201):
    ```json
    {
      "message": "User created successfully",
      "data": {
        "username": "john_doe",
        "email": "john@example.com"
      }
    }
    ```
  - **Error** (422):
    ```json
    {
      "message": "Invalid details",
      "data": { "email": ["Email is already taken"] }
    }
    ```

## 2. **User Login API**
- **Endpoint**: `/api/login/`
- **Method**: `POST`
- **Description**: Authenticates a user.
- **Request Body (JSON)**:
  ```json
  {
    "email": "john@example.com",
    "password": "strong_password"
  }
  ```
- **Response**:
  - **Success** (200):
    ```json
    {
      "message": "Login successful",
      "data": {
        "username": "john_doe"
      }
    }
    ```
  - **Error** (401):
    ```json
    {
      "message": "Invalid credentials"
    }
    ```

## 3. **Find User API**
- **Endpoint**: `/api/users/`
- **Method**: `GET`
- **Description**: Fetch a user by email or username.
- **Query Parameters**:
  - `email`: Find user by email
  - `name`: Search user by partial username
- **Example Request**:
  - `/api/users/?email=john@example.com`
  - `/api/users/?name=john`
- **Response**:
  - **Success (Single User)**:
    ```json
    {
      "username": "john_doe",
      "email": "john@example.com"
    }
    ```
  - **Success (Multiple Users)** (if using `name`):
    ```json
    [
      {
        "username": "john_doe",
        "email": "john@example.com"
      },
      {
        "username": "john_smith",
        "email": "johnsmith@example.com"
      }
    ]
    ```
  - **Empty**:
    ```json
    []
    ```

## 4. **Send Friend Request API**
- **Endpoint**: `/api/friends/send-request/{user_id}/`
- **Method**: `GET`
- **Description**: Send a friend request to another user by their `user_id`.
- **Response**:
  - **Success** (200):
    ```json
    {
      "message": "Friend request sent successfully"
    }
    ```
  - **Already Sent** (409):
    ```json
    {
      "message": "Friend request already sent"
    }
    ```
  - **Error** (Bad Request):
    ```json
    {
      "message": "Give another user"
    }
    ```

## 5. **Friend Requests API**
- **Endpoint**: `/api/friends/requests/`
- **Method**: `GET`
- **Description**: Retrieve all incoming friend requests.
- **Response**:
  - **Success** (200):
    ```json
    [
      {
        "id": 1,
        "user": {
          "username": "john_doe",
          "email": "john@example.com"
        },
        "request_status": "Sent"
      }
    ]
    ```

## 6. **Friends List API**
- **Endpoint**: `/api/friends/`
- **Method**: `GET`
- **Description**: Retrieve all accepted friends.
- **Response**:
  - **Success** (200):
    ```json
    [
      {
        "id": 1,
        "user": {
          "username": "john_doe",
          "email": "john@example.com"
        },
        "friend": {
          "username": "jane_doe",
          "email": "jane@example.com"
        },
        "request_status": "Accepted"
      }
    ]
    ```

## 7. **Change Friend Request Status API**
- **Endpoint**: `/api/friends/change-status/{request_id}/`
- **Method**: `PUT`
- **Description**: Change the status of a friend request (Accept/Reject).
- **Request Body (JSON)**:
  ```json
  {
    "request_status": "Accepted"
  }
  ```
- **Response**:
  - **Success** (200):
    ```json
    {
      "message": "Friend request Accepted successfully"
    }
    ```
  - **Error** (401):
    ```json
    {
      "message": "Unauthorized"
    }
    ```

---

### Notes:
- **Authentication**: Include an `Authorization` header with a valid JWT or session token for protected endpoints:
  ```plaintext
  Authorization: Bearer <token>
  ```
