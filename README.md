## HBnB Evolution

An AirBnB-like backend project for Holberton School, focused on clean architecture, design patterns, and technical documentation.

### 🎯 Project Overview
This part covers:
- Layered Architecture: Presentation, Business Logic, Persistence
- Design Patterns: Facade and Repository
- UML diagrams and technical documentation
- REST API design principles
## Current Phase: Part 1 - Technical Documentation
## Team Contact

| Name | Responsibility | Contact |
|------|----------------|---------|
| Munirah Alotaibi | Package Diagram | muneraenad@hotmail.com |
| Maryam Alessa | Class Diagram | roro13188@gmail.com |
| Amaal Aasiri | Sequence Diagrams | amaalmoasiri@gmail.com |

## Project Structure
holbertonschool-hbnb/
├── part1/          # Technical documentation & UML diagrams
├── part2/          # Implementation (later parts)
├── part3/          # Persistence layer (later parts)
└── README.md       # Project overview
> Note: Only `part1/` is included in this phase.

### ✅ Deliverables
- High-Level Package Diagram (3-layer architecture)
- Detailed Class Diagram (Business Logic entities)
- Sequence Diagrams (4 API interaction flows)
- Compiled Technical Documentation (PDF)

### 🏛️ Architecture Overview
The application follows a three-layer architecture:
- **Presentation Layer**: API endpoints / controllers and service interfaces
- **Business Logic Layer**: core models and business rules
- **Persistence Layer**: repositories / data access and database operations

Communication between layers is facilitated through the **Facade Pattern**.

### 🏗️ Core Entities
- **User**: user management
- **Place**: property listings (location, pricing, etc.)
- **Review**: feedback and ratings for places
- **Amenity**: reusable place features (WiFi, Pool, etc.)

### 📚 Documentation
All technical documentation is located in the `part1/` directory:
- Package diagram (architecture overview)
- Class diagram (entities and relationships)
- Sequence diagrams (key API operations)
- Full technical specifications (PDF)

### 🔧 Technologies
- **Diagrams**: Mermaid.js (renders natively on GitHub)
- **Version Control**: Git & GitHub
- **Documentation**: Markdown, PDF
- **Implementation (Part 2+)**: Python 3.x
## Contributing
This project is part of the Holberton School curriculum.

## Academic Context
- **School:** Holberton School Saudi Arabia
- **Program:** Advanced Backend Specialization
- **Project:** HBnB Evolution — Part 1 (Technical Documentation)
- **Date:** February 2026

## Part 2: Flask REST API + Business Logic (Facade & In-Memory)

## Project Overview (Part 2 Tasks)

- **Task 0:** Initialize the project structure (Presentation/Business Logic/Persistence), set up Flask-RESTx, in-memory repository, and Facade skeleton.
- **Task 1:** Implement core models (User, Place, Review, Amenity) with validation and relationships.
- **Task 2:** Build User endpoints (POST/GET/PUT + list) via Facade, excluding passwords from responses.
- **Task 3:** Build Amenity endpoints (POST/GET/PUT + list) via Facade.
- **Task 4:** Build Place endpoints (POST/GET/PUT + list), validate price/lat/lon, and include owner + amenities in responses.
- **Task 5:** Build Review endpoints (POST/GET/PUT/DELETE), validate review text, link reviews to user + place, and support retrieving place reviews.
- **Task 6:** Test and validate all endpoints (Swagger/cURL + automated tests) and produce a testing report.

## Technologies / Techniques (Part 2)

- **Python (OOP):** building core models (User/Place/Review/Amenity) with validation and relationships.
- **Flask:** lightweight web framework to run the backend service.
- **Flask-RESTx:** RESTful API structure + Swagger documentation + request/response models.
- **Facade Pattern:** single entry point between API layer and business logic/persistence.
- **Repository Pattern (In-Memory):** temporary persistence layer for CRUD operations (replaced by SQLAlchemy in Part 3).
- **Serialization:** converting models to JSON responses (including related/extended attributes).
- **Testing:** manual testing via **Swagger/cURL** + automated tests using **pytest/unittest**.
- **Git/GitHub Workflow:** team collaboration, commits, branches, and code reviews.

## Academic Context
- **School:** Holberton School Saudi Arabia
- **Program:** Advanced Backend Specialization
- **Project:** HBnB Evolution - Part 2 (Business Logic & API)
- **Date:** February 2026

## Part 3: Database Integration & Authentication

### Project Overview

| Task | Description |
|------|-------------|
| **Task 0** | Modify App Factory + Config Integration |
| **Task 1** | User Model + Password Hashing (bcrypt) |
| **Task 2** | JWT Authentication Setup |
| **Task 3** | Authenticated User Access Endpoints |
| **Task 4** | Administrator Access Endpoints |
| **Task 5** | Implement SQLAlchemy Repository |
| **Task 6** | Map User Entity to SQLAlchemy |
| **Task 7** | Map Place, Review, Amenity Entities |
| **Task 8** | Map Relationships Between Entities |
| **Task 9** | SQL Scripts (Schema + Initial Data) |
| **Task 10** | ER Diagram (Mermaid.js) |

---

### Tech Stack

| Technology | Purpose |
|------------|---------|
| **SQLAlchemy** | ORM for database persistence |
| **Flask-JWT-Extended** | JWT authentication |
| **Flask-Bcrypt** | Password hashing |
| **SQLite/MySQL** | Development & production databases |
| **Repository Pattern** | Data access abstraction |
| **Facade Pattern** | Business logic layer |
| **Mermaid.js** | ER diagram visualization |

---
## Academic Context
School: Holberton School Saudi Arabia

Program: Advanced Backend Specialization

Project: HBnB Evolution - Part 3

Date: March 2026
