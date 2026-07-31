# CareerSprint

> A simple way to keep track of job and internship applications in one place.

CareerSprint is a web application for **students and job seekers** who want to stay organized during the hiring process. Instead of relying on spreadsheets, sticky notes, or memory, it helps users record each application, track progress, save interview details, keep referral notes, and store resumes — all in one clean workspace.

The goal is simple: **users should be able to manage their applications without missing interviews, assessments, or opportunities.**

---

## Table of Contents

- [Features](#features)
- [Application Status Pipeline](#application-status-pipeline)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Clone & Install](#1-clone--install)
  - [2. Configure Environment](#2-configure-environment)
  - [3. Set Up the Database](#3-set-up-the-database)
  - [4. Seed Demo Data (Optional)](#4-seed-demo-data-optional)
  - [5. Run the Application](#5-run-the-application)
- [Screens](#screens)
- [API Reference](#api-reference)
- [Database Design](#database-design)
- [Authentication & Security](#authentication--security)
- [Business Rules](#business-rules)
- [Demo Credentials](#demo-credentials)
- [Future Enhancements](#future-enhancements)
- [Out of Scope](#out-of-scope)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### User Authentication
- Create an account
- Log in and log out securely (JWT-based)
- Personal, per-user dashboard

### Job Application Management
Users can:
- **Add** a new application
- **View** all applications
- **Update** application details
- **Delete** an application

Each application includes:
- Company name
- Job role
- Application date
- Source (LinkedIn, Internshala, company portal, referral, etc.)
- Current status
- Notes (recruiter conversations, preparation, feedback)

### Application Status Tracking
Applications move through the hiring process in stages:

```text
Applied
   │
   ▼
OA Scheduled
   │
   ▼
OA Completed
   │
   ▼
Interview
   │
   ├──────────────► Rejected
   │
   ▼
Offer
```

Possible statuses:

| Status | Meaning |
| ------ | ------- |
| `Applied` | Application submitted |
| `OA Scheduled` | Online assessment scheduled |
| `OA Completed` | Online assessment finished |
| `Interview` | In the interview stage |
| `Offer` | Received an offer |
| `Rejected` | Not selected |
| `Withdrawn` | Withdrew the application |

### Interview Round Tracking
When an application reaches the **Interview** stage, users can add interview rounds with:
- Round number
- Round type (technical screen, on-site, HR, etc.)
- Interview date
- Result (`Selected`, `Rejected`, `Awaiting Result`, `On Hold`)
- Notes

### Referral Tracking
Track referrals per application:
- Referrer name & email
- Relationship
- Date referred
- Status (`Pending`, `Confirmed`, `Not Responded`, `Declined`)
- Notes

### Resume Repository
- Upload resumes (PDF, DOCX, etc.)
- Download & delete them anytime
- Each user has their own private resume list

### Search & Filter
- Search applications by **company name**
- Filter by **status** to find opportunities that need follow-up

### Dashboard
Shows at a glance:
- Total applications
- Applications in interview
- Offers received
- Rejections

### Landing Page
A polished marketing landing page at `/` with a hero section, feature grid, and a visual status pipeline — plus a split-screen login/register experience.

---

## Tech Stack

| Layer | Technology |
| ----- | ---------- |
| **Frontend** | HTML5, CSS3, JavaScript (Jinja2 templates) |
| **Web Server / SSR** | Flask |
| **REST API** | FastAPI (Uvicorn) |
| **ORM** | SQLAlchemy 2.0 |
| **Database** | MySQL (auto-falls back to SQLite) |
| **Auth** | JWT (`python-jose`) + `bcrypt` password hashing |
| **Validation** | Pydantic 2 |
| **Tools** | Git, GitHub, Maven (repo history), Postman |

---

## Architecture

CareerSprint runs **two servers side by side**:

```text
Browser
   │
   ▼
┌────────────────────┐     HTTP (requests)     ┌─────────────────────────┐
│  Flask (port 5000) │ ──────────────────────► │  FastAPI (port 8000)    │
│  Server-rendered   │ ◄────────────────────── │  REST API + Business    │
│  Jinja2 templates  │      JSON responses     │  Logic + Auth (JWT)     │
└────────────────────┘                         └────────────┬────────────┘
                                                             │ SQLAlchemy
                                                             ▼
                                                    ┌──────────────────┐
                                                    │  MySQL / SQLite  │
                                                    └──────────────────┘
```

1. **Flask** handles routing, sessions, template rendering, file uploads, and calls the FastAPI backend with the user's JWT token.
2. **FastAPI** exposes the REST API, validates requests with Pydantic, enforces authentication, and talks to the database via SQLAlchemy.
3. **Database** — MySQL by default; if MySQL is unreachable, the app **automatically falls back to SQLite** (`careersprint.db`), so development always works.

Run both with a single command: `python run.py` (see [Getting Started](#getting-started)).

---

## Project Structure

```text
Product-Revamp/
├── app/
│   ├── __init__.py               # FastAPI app factory + router mounting
│   ├── config.py                 # Env-based configuration
│   ├── database.py               # SQLAlchemy engine, session, Base
│   ├── models.py                 # ORM models: User, Application, InterviewRound, Resume, Referral
│   ├── schemas.py                # Pydantic request/response schemas
│   ├── flask_app.py              # Flask frontend (routes + templates)
│   ├── api/
│   │   ├── auth.py               # POST /api/auth/register, /login, GET /me
│   │   ├── applications.py       # CRUD + dashboard stats
│   │   ├── interviews.py         # Interview round CRUD
│   │   ├── referrals.py          # Referral CRUD
│   │   └── resumes.py            # Upload / list / download / delete
│   ├── services/                 # Business logic layer
│   │   ├── auth_service.py       # bcrypt hashing, JWT create/decode
│   │   ├── application_service.py
│   │   ├── interview_service.py
│   │   ├── referral_service.py
│   │   └── resume_service.py     # File storage in uploads/resumes
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css         # App shell, dashboard, auth styles
│   │   │   └── landing.css       # Landing page styles
│   │   └── js/
│   └── templates/
│       ├── base.html             # App shell (sidebar) + auth layout
│       ├── landing.html          # Marketing landing page
│       ├── dashboard.html
│       ├── applications/         # list, form, detail
│       ├── auth/                 # login, register
│       ├── interviews/           # interview round forms
│       ├── referrals/            # referral forms
│       └── resumes/              # resume repository
├── database/                     # DB-related files
├── uploads/resumes/              # Uploaded resume files (stored server-side)
├── product_brief.md              # Original product specification
├── requirements.txt              # Python dependencies
├── seed.py                       # Demo data seeder
└── run.py                        # Launches FastAPI + Flask together
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **MySQL** (optional — the app falls back to SQLite if MySQL isn't running)
- Git (optional)

### 1. Clone & Install

```bash
git clone <your-repo-url> Product-Revamp
cd Product-Revamp

# Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate      # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root (a `.env` is already provided; adjust as needed):

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=careersprint
SECRET_KEY=your_jwt_secret
FLASK_SECRET_KEY=your_flask_session_secret
API_BASE_URL=http://localhost:8000
```

> **Note:** Change `SECRET_KEY` and `FLASK_SECRET_KEY` to strong random values before deploying. Never commit real secrets.

### 3. Set Up the Database

Tables are created **automatically** on startup (`Base.metadata.create_all`). Just make sure your MySQL database exists:

```sql
CREATE DATABASE careersprint;
```

If MySQL is unavailable, the app automatically creates and uses a local SQLite file (`careersprint.db`) — no extra setup needed.

### 4. Seed Demo Data (Optional)

```bash
python seed.py
```

This creates two demo users with sample applications and interview rounds (see [Demo Credentials](#demo-credentials)).

### 5. Run the Application

**Option A — one command (starts both servers):**

```bash
python run.py
```

**Option B — two terminals:**

```bash
# Terminal 1: FastAPI backend
python -m uvicorn app.__init__:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Flask frontend
python -m flask --app app.flask_app run --host 0.0.0.0 --port 5000 --debug
```

Then open:

| URL | What it is |
| --- | ---------- |
| `http://localhost:5000/` | Landing page |
| `http://localhost:5000/login` | Login page |
| `http://localhost:5000/register` | Registration page |
| `http://localhost:8000/docs` | FastAPI interactive API docs (Swagger UI) |
| `http://localhost:8000/api/health` | API health check |

---

## Screens

| Screen | Description |
| ------ | ----------- |
| Landing | Marketing page: hero, features, status pipeline, CTAs |
| Login / Register | Split-screen auth with brand panel |
| Dashboard | Stats cards (total, interview, offers, rejections) + recent applications + search/filter |
| Application List | All applications, searchable & filterable |
| Add / Edit Application | Form with company, role, date, source, status, notes |
| Application Details | Full details, status timeline, interview rounds, referrals |
| Interview Tracker | Rounds per application with result badges |
| Resumes | Upload, list, download, delete |

---

## API Reference

All endpoints (except register/login) require an `Authorization: Bearer <token>` header.

### Authentication

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `POST` | `/api/auth/register` | Create account → returns `{user, token}` |
| `POST` | `/api/auth/login` | Log in → returns `{user, token}` |
| `GET` | `/api/auth/me` | Get the current user |

### Applications

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `POST` | `/api/applications` | Create an application |
| `GET` | `/api/applications` | List user's applications (`?search=&status=`) |
| `GET` | `/api/applications/dashboard` | Dashboard stats (totals, interviews, offers, rejections) |
| `GET` | `/api/applications/{id}` | View one application |
| `PUT` | `/api/applications/{id}` | Update an application |
| `DELETE` | `/api/applications/{id}` | Delete an application (cascades to rounds & referrals) |

### Interview Rounds

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `POST` | `/api/interviews/{app_id}` | Add a round (only when status = Interview) |
| `GET` | `/api/interviews/{app_id}` | List rounds for an application |
| `PUT` | `/api/interviews/{app_id}/{round_id}` | Update a round |
| `DELETE` | `/api/interviews/{app_id}/{round_id}` | Delete a round |

### Referrals

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `POST` | `/api/referrals/{app_id}` | Add a referral |
| `GET` | `/api/referrals/{app_id}` | List referrals for an application |
| `PUT` | `/api/referrals/{app_id}/{referral_id}` | Update a referral |
| `DELETE` | `/api/referrals/{app_id}/{referral_id}` | Delete a referral |

### Resumes

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `POST` | `/api/resumes/upload` | Upload a resume (multipart form, field name `file`) |
| `GET` | `/api/resumes` | List user's resumes |
| `GET` | `/api/resumes/{id}/download` | Download a resume |
| `DELETE` | `/api/resumes/{id}` | Delete a resume |

### Misc

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET` | `/api/health` | Health check → `{"status": "ok"}` |

Interactive docs: `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc`.

---

## Database Design

### Entity Relationship

```text
User
 │
 │ 1
 │
 ▼
Applications
 │
 │ 1
 │
 ├────► Interview Rounds
 │
 └────► Referrals

User
 │
 │ 1
 │
 ▼
Resumes
```

- One user can have many applications.
- One application can have many interview rounds.
- One application can have many referrals.
- One user can have many resumes.

### Tables

**users**

| Field | Type | Notes |
| ----- | ---- | ----- |
| user_id | Integer | PK, auto-increment |
| name | String(255) | required |
| email | String(255) | unique, required |
| password | String(255) | bcrypt hash |
| created_at | TIMESTAMP | auto |

**applications**

| Field | Type | Notes |
| ----- | ---- | ----- |
| application_id | Integer | PK |
| user_id | Integer | FK → users, ON DELETE CASCADE |
| company_name | String(255) | required |
| role | String(255) | required |
| application_date | Date | required |
| source | String(255) | optional |
| status | Enum | Applied / OA Scheduled / OA Completed / Interview / Offer / Rejected / Withdrawn |
| notes | Text | optional |
| created_at / updated_at | TIMESTAMP | auto |

**interview_rounds**

| Field | Type | Notes |
| ----- | ---- | ----- |
| round_id | Integer | PK |
| application_id | Integer | FK → applications, ON DELETE CASCADE |
| round_number | Integer | required |
| round_type | String(255) | e.g. Technical Phone Screen |
| interview_date | Date | optional |
| result | Enum | Selected / Rejected / Awaiting Result / On Hold |
| notes | Text | optional |
| created_at | TIMESTAMP | auto |

**referrals**

| Field | Type | Notes |
| ----- | ---- | ----- |
| referral_id | Integer | PK |
| application_id | Integer | FK → applications, ON DELETE CASCADE |
| referrer_name | String(255) | required |
| referrer_email | String(255) | optional |
| relationship | String(255) | optional |
| date_referred | Date | optional |
| status | Enum | Pending / Confirmed / Not Responded / Declined |
| notes | Text | optional |
| created_at | TIMESTAMP | auto |

**resumes**

| Field | Type | Notes |
| ----- | ---- | ----- |
| resume_id | Integer | PK |
| user_id | Integer | FK → users, ON DELETE CASCADE |
| filename | String(255) | unique name on disk (UUID) |
| original_name | String(255) | original filename |
| uploaded_at | TIMESTAMP | auto |

---

## Authentication & Security

- **Passwords** are hashed with **bcrypt** before storage — never stored in plain text.
- **JWT tokens** (HS256) are issued on register/login and expire after **7 days**.
- Tokens carry `user_id` and `email`; every protected endpoint verifies the token and resolves the current user.
- **Data isolation**: every query is scoped by `user_id` — users can only read/write their own applications, rounds, referrals, and resumes.
- Flask stores the JWT in the user's session cookie and forwards it as a `Bearer` token to the API.

---

## Business Rules

- Users must log in before accessing their data.
- Every application belongs to exactly one user.
- Users can only manage their own applications.
- Company name and role are required.
- Interview rounds can only be added when an application's status is `Interview`.
- An application can have multiple interview rounds.
- Interview rounds are **not** removed automatically when the application status changes.
- Deleting an application removes all related interview rounds and referrals.
- Deleting a user cascades to their applications and resumes.

---

## Demo Credentials

After running `python seed.py`:

| Email | Password |
| ----- | -------- |
| `alice@example.com` | `password123` |
| `bob@example.com` | `password123` |

Sample data includes applications across companies (Google, Microsoft, Amazon, Stripe, Meta, Apple, Netflix, Spotify) with interview rounds in various stages.

---

## Future Enhancements

- Resume repository enhancements
- Referral tracker analytics
- Calendar integration
- Deadline reminders
- Email notifications
- Dark mode
- Advanced analytics
- Export applications

---

## Out of Scope

The following are **not** part of the current version:

- LinkedIn integration
- Automatic job import
- AI interview coach
- Recruiter portal
- Company accounts
- Mobile application

---

## Contributing

This project was created as part of a **software development training assignment**. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## License

This project is intended for **educational purposes** as part of a software development training assignment.
