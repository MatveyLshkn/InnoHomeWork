# JSONPlaceholder API Clone

This project is a RESTful API that replicates the functionality of JSONPlaceholder (https://jsonplaceholder.typicode.com) with additional features including JWT authentication, structured user data storage, and containerized deployment.

## Features

- Full REST API implementation for users
- JWT-based authentication
- PostgreSQL database with SQLAlchemy ORM
- Docker and Docker Compose support
- Automatic API documentation (Swagger/OpenAPI)
- Data validation using Pydantic
- Seeded initial data from JSONPlaceholder

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Getting Started

1. Clone the repository
2. Navigate to the project directory
3. Start the application using Docker Compose:

```bash
docker-compose up --build
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /token` - Get JWT token (requires username and password)

### Users

- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get user by ID
- `POST /users/` - Create new user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

## Data Models

### User

```typescript
interface User {
  id: number;
  name: string;
  username: string;
  email: string;
  address: Address;
  phone: string;
  website: string;
  company: Company;
}
```

### Address

```typescript
interface Address {
  street: string;
  suite: string;
  city: string;
  zipcode: string;
  geo: Geo;
}
```

### Geo

```typescript
interface Geo {
  lat: string;
  lng: string;
}
```

### Company

```typescript
interface Company {
  name: string;
  catchPhrase: string;
  bs: string;
}
```

## Development

### Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/jsonplaceholder"
export JWT_SECRET_KEY="your-secret-key-here"
export JWT_ALGORITHM="HS256"
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

### Running Tests

```bash
pytest
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Input validation is performed using Pydantic models
- SQL injection protection through SQLAlchemy

## License

MIT 