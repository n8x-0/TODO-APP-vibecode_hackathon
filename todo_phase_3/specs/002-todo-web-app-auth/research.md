# Research: Todo Web App with Authentication

## Decision: Backend Framework
**Rationale**: FastAPI was chosen as the backend framework based on the feature requirements and project constraints. It provides excellent support for async operations, automatic API documentation, and integrates well with the Python ecosystem.
**Alternatives considered**: 
- Flask: More mature but less performant for async operations
- Django: More heavyweight than needed for this application

## Decision: Frontend Framework
**Rationale**: Next.js 14 was selected as the frontend framework as specified in the requirements. It provides server-side rendering, routing, and a rich ecosystem of tools.
**Alternatives considered**: 
- React with Vite: More lightweight but requires more setup
- Angular: More complex learning curve

## Decision: Database
**Rationale**: Neon Postgres was chosen as the database as specified in the requirements. It provides a modern PostgreSQL-compatible database with serverless capabilities.
**Alternatives considered**: 
- SQLite: Simpler but less scalable
- MongoDB: Different data model, doesn't match requirements

## Decision: Authentication Method
**Rationale**: Cookie-based authentication with HttpOnly cookies was chosen as specified in the requirements. This provides better security against XSS attacks compared to token storage in localStorage.
**Alternatives considered**: 
- JWT in localStorage: More common but less secure against XSS
- Session tokens in memory: Possible but cookies are more appropriate for this use case

## Decision: Password Hashing
**Rationale**: bcrypt was selected for password hashing as it's a well-established, secure method for password storage that handles salting automatically.
**Alternatives considered**: 
- Argon2: Also secure but less commonly used in Python ecosystem
- Scrypt: Secure but bcrypt is more established

## Decision: ORM/Database Access
**Rationale**: SQLAlchemy will be used as the ORM for database access as it's the most established and feature-rich ORM for Python with excellent PostgreSQL support.
**Alternatives considered**: 
- Peewee: Simpler but less feature-rich
- Raw SQL: More control but more error-prone

## Decision: Migration Tool
**Rationale**: Alembic will be used for database migrations as it's the standard migration tool for SQLAlchemy and provides excellent version control for database schemas.
**Alternatives considered**: 
- Django migrations: Only applicable if using Django
- Manual migrations: Error-prone and not recommended

## Resolution: Testing Framework
**Rationale**: pytest was chosen for backend testing as it's the most popular and feature-rich testing framework for Python. For frontend testing, Jest with React Testing Library will be used.
**Alternatives considered**: 
- unittest: Built-in but less feature-rich than pytest
- Mocha: JavaScript testing framework but pytest is more common for Python

## Resolution: Performance Goals
**Rationale**: The target response time will be under 200ms for API calls to ensure a responsive user experience. This is a standard target for web APIs.
**Alternatives considered**: 
- 100ms: More aggressive but harder to achieve consistently
- 500ms: Too slow for a good user experience

## Resolution: Scale/Scope
**Rationale**: The application will initially support up to 10,000 users, which should be sufficient for early adoption and testing. This can be scaled later as needed.
**Alternatives considered**: 
- 1,000 users: Too limited for growth
- 100,000 users: Over-engineering for initial version