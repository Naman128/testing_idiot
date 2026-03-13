# Place Review API

A production-quality REST API backend for a mobile application that allows authenticated users to review places (shops, doctors, restaurants, etc.).

## Tech Stack

- **Backend Framework**: Django 4.2+
- **API Framework**: Django REST Framework
- **Database**: SQLite (for local development)
- **Authentication**: Token-based authentication

## Project Structure

```
place_review_api/
├── manage.py
├── requirements.txt
├── README.md
├── place_review_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
└── reviews/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    └── management/
        └── commands/
            └── populate_data.py
```

## Installation & Setup

### 1. Create a Virtual Environment

```bash
# Navigate to the project directory
cd place_review_api

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Populate Test Data

```bash
# Default: 50 users, 100 places, 500 reviews
python manage.py populate_data

# Custom amounts:
python manage.py populate_data --users 100 --places 200 --reviews 1000

# Clear existing data before populating:
python manage.py populate_data --clear
```

### 6. Start the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication

All endpoints (except registration and login) require authentication using a token in the header:
```
Authorization: Token <your-token>
```

#### Register a New User
```
POST /api/auth/register/
```
**Request Body:**
```json
{
    "name": "John Doe",
    "phone_number": "+919876543210",
    "password": "yourpassword"
}
```
**Response:**
```json
{
    "message": "User registered successfully.",
    "token": "abc123...",
    "user": {
        "id": 1,
        "name": "John Doe",
        "phone_number": "+919876543210",
        "date_joined": "2025-12-28T10:00:00Z"
    }
}
```

#### Login
```
POST /api/auth/login/
```
**Request Body:**
```json
{
    "phone_number": "+919876543210",
    "password": "yourpassword"
}
```
**Response:**
```json
{
    "message": "Login successful.",
    "token": "abc123...",
    "user": {
        "id": 1,
        "name": "John Doe",
        "phone_number": "+919876543210",
        "date_joined": "2025-12-28T10:00:00Z"
    }
}
```

#### Logout
```
POST /api/auth/logout/
```
**Headers:** `Authorization: Token <your-token>`

**Response:**
```json
{
    "message": "Logout successful."
}
```

#### Get User Profile
```
GET /api/auth/profile/
```
**Headers:** `Authorization: Token <your-token>`

---

### Reviews

#### Add a Review
```
POST /api/reviews/
```
**Headers:** `Authorization: Token <your-token>`

**Request Body:**
```json
{
    "place_name": "The Royal Restaurant",
    "place_address": "123, MG Road, Mumbai, Maharashtra - 400001",
    "rating": 5,
    "text": "Excellent food and service!"
}
```
**Note:** If the place doesn't exist, it will be created automatically.

**Response:**
```json
{
    "message": "Review added successfully.",
    "review": {
        "id": 1,
        "rating": 5,
        "text": "Excellent food and service!",
        "created_at": "2025-12-28T10:00:00Z",
        "reviewer_name": "John Doe"
    },
    "place": {
        "id": 1,
        "name": "The Royal Restaurant",
        "address": "123, MG Road, Mumbai, Maharashtra - 400001"
    }
}
```

#### Get My Reviews
```
GET /api/reviews/my/
```
**Headers:** `Authorization: Token <your-token>`

---

### Places

#### Search Places
```
GET /api/places/search/
```
**Headers:** `Authorization: Token <your-token>`

**Query Parameters:**
- `name` (optional): Search by place name (exact matches shown first, then partial)
- `min_rating` (optional): Filter by minimum average rating (1-5)

**Examples:**
```
GET /api/places/search/?name=Royal
GET /api/places/search/?min_rating=4
GET /api/places/search/?name=Restaurant&min_rating=4
```

**Response:**
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "Royal Restaurant",
            "address": "123, MG Road, Mumbai",
            "average_rating": 4.5
        },
        {
            "id": 2,
            "name": "The Royal Cafe",
            "address": "456, Park Street, Delhi",
            "average_rating": 4.2
        }
    ]
}
```

#### Get Place Details
```
GET /api/places/<place_id>/
```
**Headers:** `Authorization: Token <your-token>`

**Response:**
```json
{
    "id": 1,
    "name": "Royal Restaurant",
    "address": "123, MG Road, Mumbai, Maharashtra - 400001",
    "average_rating": 4.5,
    "review_count": 10,
    "reviews": [
        {
            "id": 5,
            "rating": 5,
            "text": "My review (shown first if current user reviewed)",
            "created_at": "2025-12-28T10:00:00Z",
            "reviewer_name": "John Doe"
        },
        {
            "id": 4,
            "rating": 4,
            "text": "Great food!",
            "created_at": "2025-12-27T15:00:00Z",
            "reviewer_name": "Jane Smith"
        }
    ]
}
```

**Note:** Reviews are sorted with the current user's review first (if exists), followed by other reviews sorted by newest first.

---

## Data Models

### User
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | User's full name |
| phone_number | String | Unique phone number (used for authentication) |
| date_joined | DateTime | Account creation timestamp |

### Place
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Place name |
| address | Text | Full address |
| created_at | DateTime | Creation timestamp |

**Unique Constraint:** Combination of (name + address) must be unique.

### Review
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user | ForeignKey | Reference to User |
| place | ForeignKey | Reference to Place |
| rating | Integer | Rating from 1 to 5 |
| text | Text | Optional review text |
| created_at | DateTime | Review timestamp |

---

## Testing with cURL

### Register
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "phone_number": "+919876543210", "password": "testpass123"}'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+919876543210", "password": "testpass123"}'
```

### Add Review (replace TOKEN with your actual token)
```bash
curl -X POST http://127.0.0.1:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token TOKEN" \
  -d '{"place_name": "Test Cafe", "place_address": "123 Main St", "rating": 5, "text": "Great!"}'
```

### Search Places
```bash
curl -X GET "http://127.0.0.1:8000/api/places/search/?name=Cafe&min_rating=4" \
  -H "Authorization: Token TOKEN"
```

---

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` with your superuser credentials to manage:
- Users
- Places
- Reviews

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK`: Successful GET/PATCH request
- `201 Created`: Successful POST request (new resource created)
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Resource not found

Error responses include descriptive messages:
```json
{
    "error": "Place not found."
}
```
or
```json
{
    "phone_number": ["A user with this phone number already exists."]
}
```
