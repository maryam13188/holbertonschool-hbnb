# HBnB Evolution - Part 3

## Introduction
**HBnB Evolution - Part 3** represents the transition of the project from a basic prototype into a database-driven web application.  
Building on the work completed in previous phases, this stage focuses on connecting the application to a real persistence layer using **SQLAlchemy**, implementing secure authentication with **JWT**, and defining entity relationships in a structured relational model.

This part is designed to strengthen the overall architecture of the project by separating concerns into clear layers: API, business logic, and persistence. It also introduces better scalability and maintainability practices commonly used in real-world backend systems.

## Features
- App Factory configuration
- SQLAlchemy repository implementation
- User model with password hashing
- JWT-based authentication
- Protected and admin-only endpoints
- Entity mapping for User, Place, Review, and Amenity
- Relationship mapping between entities
- SQL scripts for database setup
- ER diagram documentation

## Architecture Design
The application is organized into three main layers:

- **Presentation Layer**: Handles API routes and HTTP requests
- **Business Logic Layer**: Contains the core rules and service logic
- **Persistence Layer**: Manages data access through repositories and database models

## Project Structure

```text
holbertonschool-hbnb/
├── part1/
├── part2/
├── part3/
│   ├── run.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env
│   ├── .gitignore
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── extensions.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── places.py
│   │   │       ├── reviews.py
│   │   │       └── amenities.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base_model.py
│   │   │   ├── user.py
│   │   │   ├── place.py
│   │   │   ├── review.py
│   │   │   └── amenity.py
│   │   │
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── repository.py
│   │   │   ├── in_memory_repository.py
│   │   │   └── sqlalchemy_repository.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       └── facade.py
│   │
│   ├── sql_scripts/
│   │   ├── schema.sql
│   │   └── initial_data.sql
│   │
│   ├── docs/
│   │   └── er_diagram.md
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   ├── test_places.py
│   │   └── test_reviews.py
│   │
│   └── instance/
│       └── hbnb_dev.db
│
└── README.md
```
## Task Completion by Team Member

### 🔵 Munirah — Task 0, 5, 9
| Task | Description | Status |
|------|-------------|--------|
| 0 | Modify App Factory + Config Integration | ✅ Complete |
| 5 | Implement SQLAlchemy Repository | ✅ Complete |
| 9 | SQL Scripts (Schema + Initial Data) | ✅ Complete |

### 🟣 Maryam — Task 1, 6, 7, 10
| Task | Description | Status |
|------|-------------|--------|
| 1 | User Model + Password Hashing (bcrypt) | ✅ Complete |
| 6 | Map User Entity to SQLAlchemy | ✅ Complete |
| 7 | Map Place, Review, Amenity Entities | ✅ Complete |
| 10 | ER Diagram (Mermaid.js) | ✅ Complete |

### 🟢 Amal — Task 2, 3, 4, 8
| Task | Description | Status |
|------|-------------|--------|
| 2 | JWT Authentication Setup | ✅ Complete |
| 3 | Authenticated User Access Endpoints | ✅ Complete |
| 4 | Administrator Access Endpoints | ✅ Complete |
| 8 | Map Relationships Between Entities | ✅ Complete |

