# Healthcare Management Backend

A REST API for managing patients, doctors, and patient-doctor assignments. Built with Django, Django REST Framework, PostgreSQL, and JWT authentication.

## Tech stack

- Python, Django, Django REST Framework
- PostgreSQL (via psycopg)
- djangorestframework-simplejwt for JWT auth
- python-dotenv for environment variables

## Features

- Register and log in with email and password
- JWT access and refresh tokens
- Patients: each user can only see and manage their own patients
- Doctors: shared directory, only the creator can edit or delete a doctor
- Mappings: assign doctors to patients you own, duplicates blocked by a database constraint

## Project structure

```
Healthcare backend assignment/
  README.md
  .gitignore
  backend/
    manage.py
    requirements.txt
    .env.example
    config/       settings and root URLs
    accounts/     custom user model, register, login
    patients/     patient model and endpoints
    doctors/      doctor model, endpoints, permission class
    mappings/     patient-doctor mapping model and endpoints
```

## Setup (Windows PowerShell)

### 1. Clone the repository

```powershell
git clone https://github.com/Mumal-Singh/Healthcare_backend_coderbyte.git
cd Healthcare_backend_coderbyte\backend
```

### 2. Create a virtual environment and install dependencies

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Create the PostgreSQL database

```powershell
psql -U postgres -h localhost
```

```sql
CREATE USER healthcare_user WITH PASSWORD 'your_password_here';
CREATE DATABASE healthcare_db OWNER healthcare_user;
\q
```

### 4. Configure environment variables

```powershell
Copy-Item .env.example .env
```

Open `.env` and fill in the values (see the table below). Generate a secret key with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Run migrations and start the server

```powershell
python manage.py migrate
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

## Environment variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key, keep it private | long random string |
| `DEBUG` | `True` for development, `False` otherwise | `True` |
| `ALLOWED_HOSTS` | Comma-separated hostnames | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | `healthcare_db` |
| `DB_USER` | PostgreSQL user | `healthcare_user` |
| `DB_PASSWORD` | PostgreSQL password | your password |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |

The `.env` file is ignored by Git. Never commit it.

## Authentication

Protected endpoints need this header:

```
Authorization: Bearer <access_token>
```

The access token lasts 30 minutes and the refresh token lasts 1 day. When the access token expires, request a new one from `/api/auth/token/refresh/`.

## API reference

All request and response bodies are JSON.

### Auth

| Method | URL | Token required | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | No | Register a user |
| POST | `/api/auth/login/` | No | Log in, returns `access` and `refresh` |
| POST | `/api/auth/token/refresh/` | No | Exchange a refresh token for a new access token |

Register body:

```json
{ "name": "Test User", "email": "test@example.com", "password": "StrongPass123!" }
```

Login body:

```json
{ "email": "test@example.com", "password": "StrongPass123!" }
```

### Patients (token required)

| Method | URL | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/<id>/` | Get one of your patients |
| PUT | `/api/patients/<id>/` | Full update |
| PATCH | `/api/patients/<id>/` | Partial update |
| DELETE | `/api/patients/<id>/` | Delete a patient |

Body:

```json
{
  "name": "Ravi Kumar",
  "age": 45,
  "gender": "M",
  "phone": "9876543210",
  "address": "Jaipur",
  "medical_notes": "Mild hypertension"
}
```

`gender` must be `M`, `F`, or `O`. `age` must be between 0 and 120. `phone`, `address`, and `medical_notes` are optional.

### Doctors (token required)

| Method | URL | Description |
|---|---|---|
| POST | `/api/doctors/` | Add a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Get one doctor |
| PUT / PATCH | `/api/doctors/<id>/` | Update (creator only) |
| DELETE | `/api/doctors/<id>/` | Delete (creator only) |

Body:

```json
{
  "name": "Anita Sharma",
  "specialization": "Cardiology",
  "phone": "9123456780",
  "email": "anita@hospital.com",
  "years_of_experience": 12
}
```

### Mappings (token required)

| Method | URL | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to one of your patients |
| GET | `/api/mappings/` | List mappings for your patients |
| GET | `/api/mappings/<patient_id>/` | List the doctors assigned to a patient |
| DELETE | `/api/mappings/<id>/` | Remove an assignment |

Body:

```json
{ "patient": 1, "doctor": 1 }
```

Note: in `GET /api/mappings/<patient_id>/` the number is a **patient id**. In `DELETE /api/mappings/<id>/` the number is a **mapping id**. A mapping has its own id, separate from the patient and doctor it links.

## Authorization rules

| Resource | Rule | Response when violated |
|---|---|---|
| Patients | Only the owner can read, edit, or delete | `404` (another user's patient looks like it does not exist) |
| Doctors | Anyone logged in can read and create, only the creator can edit or delete | `403` |
| Mappings | Only the owner of the patient can create, view, or delete | `400` on create, `404` otherwise |

## Status codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 204 | Deleted, no body |
| 400 | Invalid input or duplicate data |
| 401 | Missing, invalid, or expired token |
| 403 | Logged in but not allowed |
| 404 | Not found, or not yours |

## Testing

The endpoints were tested manually with Postman, including:

- invalid credentials, duplicate emails, and unauthenticated access
- cross-user access to patients and doctors
- duplicate mapping assignments

## Notes

- Passwords are hashed with Django's default hasher and never returned by the API.
- A database `UniqueConstraint` on `(patient, doctor)` prevents duplicate assignments.
- Secrets are read from environment variables, and `.env` is excluded by `.gitignore`.