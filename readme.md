# Expense Tracker API

## Project Overview
Python-based solution for the [Expense Tracker API](https://roadmap.sh/projects/expense-tracker-api) challenge from [roadmap.sh](https://roadmap.sh/).

This project is a Django REST Framework-based API that allows users to manage their personal expenses. It supports user registration and authentication via JWT, as well as full CRUD functionality for managing expenses. Users can also filter expenses by specific date ranges for better financial tracking.


## Features
* **User Registration and Authentication**: Register as a new user and log in to receive a JWT access token. All API endpoints are protected and only accessible to authenticated users.

* **Expense Creation and Tracking**: Add new expenses with detailed information including title, amount, note, category, and date. Each expense is tied to the authenticated user.

* **Expense Filtering**: Retrieve a list of past expenses with optional filtering by category, past week, past month, last 3 months, or a custom date range.

* **Expense Modification**: Update details of any existing expense that belongs to the authenticated user.

* **Expense Deletion**: Remove any expense from list with a simple DELETE request.

* **Preset Categories**: Classify expenses into one of the preset categories: Grocery, Leisure, Electronics, Utilities, Clothing, Health, or Other.

## Technologies Used
* **Django**: Python web framework.
* **Django REST Framework**: Toolkit for building Web APIs.
* **Simple JWT**: Library used to generate and verify JSON Web Tokens.
* **PostgreSQL (psycopg2-binary)**: Relational database system used for storing user and expense data, connected via the psycopg2 adapter.
* **django-filter**: Adds filtering capabilities to Django REST Framework, enabling date-based and category-based queries.

## API Usage
### Base URL
The API is hosted locally at:
`http://localhost:8000/api/`

### Authentication Endpoints

| Endpoint                  | Method | Description                           |
|---------------------------|--------|---------------------------------------|
| /auth/register/           | POST   | Register a new user                   |
| /auth/token/              | POST   | Obtain JWT access and refresh token   |
| /auth/token/refresh/      | POST   | Refresh access token                  |
| /auth/token/verify/       | POST   | Verify validity of a token            |


### Expense Endpoints

| Endpoint                 | Method | Description                            |
|--------------------------|--------|----------------------------------------|
| /user/expense/           | GET    | List all user expenses                 |   
| /user/expense/           | POST   | Create a new expense                   |  
| /user/expense/<id>/      | GET    | Retrieve details of a specific expense |       
| /user/expense/<id>/      | PUT    | Update an existing expense             |
| /user/expense/<id>/      | DELETE | Delete an expense                      |


### Query Parameters for Filtering
* `past_week` – past 7 days
* `past_month` – past 30 days
* `last_3_months` – past 90 days
* `start_date` and `end_date` (optional): Custom date range in the format YYYY-MM-DD. Both values must be provided together.
* `category` (optional): Expenses are filtered by category name in a case insensitive manner

### Example Request
Retrieve details of a specific expense
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1MjMyODY4LCJpYXQiOjE3NDUyMjYwNzcsImp0aSI6Ijc5YWQwZmU1YzJiMjQ1NmViMGUzZjQ4NzZiZjkxOGY2IiwidXNlcl9pZCI6M30.LmhAtNioGz2MaCeAqlSy5vb3XqaKL_SyKt6ArHeUyPQ" "http://localhost:8000/api/user/expense/3/"
```

### Response Format
```json
{
    "id": 3,
    "title": "Expense_59",
    "amount": "89.14",
    "note": "Note_88",
    "category": "clothing",
    "date": "2025-03-07",
    "created_at": "2025-04-19T10:28:31.899000Z",
    "updated_at": "2025-04-19T10:28:31.899000Z"
}
```

## Installation
### Prerequisites
* **Python 3.10+**
* **PostgreSQL**: Check that PostgreSQL is installed and running on your computer.

### Steps
1. **Clone the Repository**:
```bash
  git https://github.com/Web-energumen/Expense-Tracker-API.git
  cd Expense-Tracker-API
```

2. **Set Up Virtual Environment**:
```bash
  python3 -m venv venv
  source venv/bin/activate
```

3. **Install Dependencies**:
```bash
  pip install -r requirements.txt
```

4. **Set Up PostgreSQL Database**: Make sure PostgreSQL is installed and running. Create a database and a user for the project:
```bash
  sudo -u postgres psql
  CREATE DATABASE your_database_name;
  CREATE USER your_database_user WITH PASSWORD 'your_database_password';
  \c your_database_name
  GRANT ALL ON SCHEMA public TO your_database_user;
```

5. **Configure Environment Variables:**: Create a .env file in the root directory and add:
```
  DB_NAME=your_database_name
  DB_USER=your_database_user
  DB_PASSWORD=your_database_password
  DB_HOST=localhost
  DB_PORT=5432
```

6. **Apply Migrations**:
``` bash
  python3 manage.py migrate
```

7. Test the API:
``` bash
  curl -H "Authorization: Bearer YOUR_JWT_TOKEN" "http://localhost:8000/api/user/expense/"
```
