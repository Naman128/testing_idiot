# Place Review API - Testing Guide

This guide provides detailed examples for testing all API endpoints with sample inputs and expected outputs.

## Base URL
```
http://127.0.0.1:8000
```

## 🔑 Authentication - IMPORTANT!

All endpoints (except Register and Login) require **Token authentication**.

### How to Set the Authorization Header

The Authorization header **MUST** include the word `Token` followed by a **space** and then your token:

```
Authorization: Token <your_token_here>
```

### ⚠️ Common Mistake

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| `Authorization: e174aaee7fc13778...` | `Authorization: Token e174aaee7fc13778...` |
| `Authorization: Bearer e174aaee7fc13778...` | `Authorization: Token e174aaee7fc13778...` |

### Example with Real Token

If your token is `e174aaee7fc13778f87cf427b2d54896dc92817f`, the header should be:

```
Authorization: Token e174aaee7fc13778f87cf427b2d54896dc92817f
```

### Setting Token in Different Tools

#### Thunder Client (VS Code Extension)
1. Go to **Headers** tab
2. Add:
   - **Key:** `Authorization`
   - **Value:** `Token e174aaee7fc13778f87cf427b2d54896dc92817f`

#### Postman
1. Go to **Headers** tab
2. Add:
   - **Key:** `Authorization`
   - **Value:** `Token e174aaee7fc13778f87cf427b2d54896dc92817f`

Or use **Auth** tab → Select **API Key** → Key: `Authorization`, Value: `Token <token>`, Add to: Header

#### cURL
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Token e174aaee7fc13778f87cf427b2d54896dc92817f"
```

#### Swagger UI
1. Click **Authorize** button (top right)
2. In the input field, enter: `Token e174aaee7fc13778f87cf427b2d54896dc92817f`
3. Click **Authorize**

#### Python Requests
```python
import requests

headers = {
    'Authorization': 'Token e174aaee7fc13778f87cf427b2d54896dc92817f'
}
response = requests.get('http://127.0.0.1:8000/api/auth/profile/', headers=headers)
print(response.json())
```

#### JavaScript Fetch
```javascript
fetch('http://127.0.0.1:8000/api/auth/profile/', {
    headers: {
        'Authorization': 'Token e174aaee7fc13778f87cf427b2d54896dc92817f'
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🔐 Authentication Endpoints

### 1. Register User

**Endpoint:** `POST /api/auth/register/`

**Description:** Register a new user with name, phone number, and password.

**Request Body:**
```json
{
    "name": "John Doe",
    "phone_number": "9876543210",
    "password": "mypassword123"
}
```

**Expected Response (201 Created):**
```json
{
    "message": "User registered successfully.",
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "user": {
        "id": 1,
        "name": "John Doe",
        "phone_number": "9876543210",
        "date_joined": "2025-12-28T12:00:00Z"
    }
}
```
```

**Error Response (400 Bad Request) - Duplicate Phone:**
```json
{
    "phone_number": [
        "A user with this phone number already exists."
    ]
}
```

**Error Response (400 Bad Request) - Missing Fields:**
```json
{
    "name": ["This field is required."],
    "phone_number": ["This field is required."],
    "password": ["This field is required."]
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "phone_number": "9876543210", "password": "mypassword123"}'
```

**PowerShell Example:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/register/" -Method POST -ContentType "application/json" -Body '{"name": "John Doe", "phone_number": "9876543210", "password": "mypassword123"}'
```

---

### 2. Login User

**Endpoint:** `POST /api/auth/login/`

**Description:** Login with phone number and password to get authentication token.

**Request Body:**
```json
{
    "phone_number": "9876543210",
    "password": "mypassword123"
}
```

**Expected Response (200 OK):**
```json
{
    "message": "Login successful.",
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "user": {
        "id": 1,
        "name": "John Doe",
        "phone_number": "9876543210",
        "date_joined": "2025-12-28T12:00:00Z"
    }
}
```

**Error Response (400 Bad Request) - Invalid Credentials:**
```json
{
    "non_field_errors": [
        "Invalid phone number or password."
    ]
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9876543210", "password": "mypassword123"}'
```

---

### 3. Logout User

**Endpoint:** `POST /api/auth/logout/`

**Description:** Logout and invalidate the authentication token.

**Headers Required:**
```
Authorization: Token <your_token_here>
```

**Request Body:** None required

**Expected Response (200 OK):**
```json
{
    "message": "Logout successful."
}
```

**Error Response (401 Unauthorized):**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

---

### 4. Get User Profile

**Endpoint:** `GET /api/auth/profile/`

**Description:** Get the current user's profile information.

**Headers Required:**
```
Authorization: Token <your_token_here>
```

**Expected Response (200 OK):**
```json
{
    "id": 1,
    "name": "John Doe",
    "phone_number": "9876543210",
    "date_joined": "2025-12-28T12:00:00Z"
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

---

### 5. Update User Profile

**Endpoint:** `PATCH /api/auth/profile/`

**Description:** Update the current user's profile (partial update).

**Headers Required:**
```
Authorization: Token <your_token_here>
```

**Request Body (only fields you want to update):**
```json
{
    "name": "John Smith"
}
```

**Expected Response (200 OK):**
```json
{
    "id": 1,
    "name": "John Smith",
    "phone_number": "9876543210",
    "date_joined": "2025-12-28T12:00:00Z"
}
```

**cURL Example:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Smith"}'
```

---

## ⭐ Review Endpoints

### 6. Add Review

**Endpoint:** `POST /api/reviews/`

**Description:** Add a new review for a place. If the place doesn't exist, it will be created automatically.

**Headers Required:**
```
Authorization: Token <your_token_here>
```

**Request Body:**
```json
{
    "place_name": "Pizza Palace",
    "place_address": "123 Main Street, New York",
    "rating": 5,
    "text": "Amazing pizza! Best in town."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| place_name | string | Yes | Name of the place |
| place_address | string | Yes | Full address of the place |
| rating | integer | Yes | Rating from 1 to 5 |
| text | string | No | Optional review text |

**Expected Response (201 Created):**
```json
{
    "message": "Review added successfully.",
    "review": {
        "id": 1,
        "rating": 5,
        "text": "Amazing pizza! Best in town.",
        "created_at": "2025-12-28T12:00:00Z",
        "reviewer_name": "John Doe"
    },
    "place": {
        "id": 1,
        "name": "Pizza Palace",
        "address": "123 Main Street, New York"
    }
}
```

**Error Response (400 Bad Request) - Invalid Rating:**
```json
{
    "rating": [
        "Ensure this value is greater than or equal to 1."
    ]
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0" \
  -H "Content-Type: application/json" \
  -d '{"place_name": "Pizza Palace", "place_address": "123 Main Street, New York", "rating": 5, "text": "Amazing pizza!"}'
```

---

### 7. Get My Reviews

**Endpoint:** `GET /api/reviews/my/`

**Description:** Get all reviews submitted by the current authenticated user.

**Headers Required:**
```
Authorization: Token <your_token_here>
```

**Expected Response (200 OK):**
```json
{
    "count": 2,
    "reviews": [
        {
            "id": 1,
            "rating": 5,
            "text": "Amazing pizza!",
            "created_at": "2025-12-28T12:00:00Z",
            "place": {
                "id": 1,
                "name": "Pizza Palace",
                "address": "123 Main Street, New York"
            }
        },
        {
            "id": 2,
            "rating": 4,
            "text": "Great coffee!",
            "created_at": "2025-12-28T11:00:00Z",
            "place": {
                "id": 2,
                "name": "Coffee Corner",
                "address": "456 Oak Avenue"
            }
        }
    ]
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/reviews/my/ \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

---

## 📍 Place Endpoints

### 8. Search Places

**Endpoint:** `GET /api/places/search/`

**Description:** Search for places by name and/or minimum rating.

**Headers Required:**
```
Authorization: Token <your_token_here>
```

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | No | Search by place name (partial match allowed) |
| min_rating | number | No | Filter by minimum average rating (1-5) |

**Example Requests:**

1. **Search by name only:**
   ```
   GET /api/places/search/?name=Pizza
   ```

2. **Search by minimum rating only:**
   ```
   GET /api/places/search/?min_rating=4
   ```

3. **Search by both name and rating:**
   ```
   GET /api/places/search/?name=Pizza&min_rating=4
   ```

4. **Get all places:**
   ```
   GET /api/places/search/
   ```

**Expected Response (200 OK):**
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "Pizza Palace",
            "address": "123 Main Street, New York",
            "average_rating": 4.5
        },
        {
            "id": 3,
            "name": "Pizza Hut",
            "address": "789 Broadway",
            "average_rating": 3.8
        }
    ]
}
```

**Note:** 
- Exact name matches appear first, followed by partial matches
- Places without reviews will have `average_rating: null`

**Error Response (400 Bad Request) - Invalid min_rating:**
```json
{
    "error": "min_rating must be between 1 and 5."
}
```

**cURL Examples:**
```bash
# Search by name
curl -X GET "http://127.0.0.1:8000/api/places/search/?name=Pizza" \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"

# Search by rating
curl -X GET "http://127.0.0.1:8000/api/places/search/?min_rating=4" \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"

# Search by name and rating
curl -X GET "http://127.0.0.1:8000/api/places/search/?name=Pizza&min_rating=4" \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

---

### 9. Get Place Details

**Endpoint:** `GET /api/places/{place_id}/`

**Description:** Get detailed information about a specific place including all reviews.

**Headers Required:**
```
Authorization: Token <your_token_here>
```

**URL Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| place_id | integer | Yes | The ID of the place |

**Expected Response (200 OK):**
```json
{
    "id": 1,
    "name": "Pizza Palace",
    "address": "123 Main Street, New York",
    "average_rating": 4.33,
    "review_count": 3,
    "reviews": [
        {
            "id": 5,
            "rating": 5,
            "text": "My favorite place!",
            "created_at": "2025-12-28T12:00:00Z",
            "reviewer_name": "John Doe"
        },
        {
            "id": 3,
            "rating": 4,
            "text": "Great pizza!",
            "created_at": "2025-12-27T15:30:00Z",
            "reviewer_name": "Jane Smith"
        },
        {
            "id": 1,
            "rating": 4,
            "text": "Good food, nice service",
            "created_at": "2025-12-26T10:00:00Z",
            "reviewer_name": "Bob Wilson"
        }
    ]
}
```

**Note:** 
- Current user's review appears first (if they have one)
- Other reviews are sorted by newest first

**Error Response (404 Not Found):**
```json
{
    "error": "Place not found."
}
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/places/1/ \
  -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
```

---

## 🧪 Complete Testing Flow

Here's a step-by-step testing flow to try all endpoints:

### Step 1: Register a new user
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "phone_number": "1234567890", "password": "testpass123"}'
```
**Save the token from the response!**

### Step 2: Add a review (creates a new place)
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"place_name": "Awesome Cafe", "place_address": "100 Test Street", "rating": 5, "text": "Love this place!"}'
```

### Step 3: Add another review for a different place
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"place_name": "Great Restaurant", "place_address": "200 Demo Ave", "rating": 4, "text": "Good food!"}'
```

### Step 4: Get my reviews
```bash
curl -X GET http://127.0.0.1:8000/api/reviews/my/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Step 5: Search for places
```bash
# Search by name
curl -X GET "http://127.0.0.1:8000/api/places/search/?name=Cafe" \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# Search by rating
curl -X GET "http://127.0.0.1:8000/api/places/search/?min_rating=4" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Step 6: Get place details
```bash
curl -X GET http://127.0.0.1:8000/api/places/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Step 7: Get user profile
```bash
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Step 8: Logout
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## 📖 Swagger UI

For interactive API testing, visit:
- **Swagger UI:** http://127.0.0.1:8000/swagger/
- **ReDoc:** http://127.0.0.1:8000/redoc/

### How to Authenticate in Swagger:
1. First, use `/api/auth/register/` or `/api/auth/login/` to get a token
2. Click the **"Authorize"** button (lock icon at top right)
3. Enter: `Token YOUR_TOKEN_HERE`
4. Click **Authorize**
5. Now all endpoints will include authentication

---

## ❌ Common Error Responses

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```
**Solution:** Add `Authorization: Token <your_token>` header

### 401 Invalid Token
```json
{
    "detail": "Invalid token."
}
```
**Solution:** Login again to get a new token

### 400 Bad Request
```json
{
    "field_name": ["Error message here"]
}
```
**Solution:** Check the request body for missing/invalid fields

### 404 Not Found
```json
{
    "error": "Place not found."
}
```
**Solution:** Check if the resource ID exists

---

## 📊 Data Population

To populate the database with test data:

```bash
# Default: 50 users, 100 places, 500 reviews
python manage.py populate_data

# Custom amounts
python manage.py populate_data --users 30 --places 50 --reviews 200

# Clear existing data first
python manage.py populate_data --clear --users 30 --places 50 --reviews 200
```

---

## ✅ Running Tests

```bash
python manage.py test
```

Expected output:
```
Found 47 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...............................................
----------------------------------------------------------------------
Ran 47 tests in 31.207s

OK
```
