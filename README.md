# School Inventory Backend
This is a backend application for managing school inventory. It provides APIs to handle various operations related to inventory management.


```bash
git clone https://github.com/thatquietkid/school-inventory-backend.git
```

# Installation
```bash
cd school-inventory-backend
pip install -r requirements.txt
```
# Deployment in development mode
This application uses FastAPI for development. To run the application in development mode, you can use the following command:
```bash
cd app
fastapi dev main.py
```

# File Structure

```
school_inventory_backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app instance & routes mounting
│   ├── config.py              # Environment configs (e.g., DB, JWT)
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── inventory.py
│   │   ├── booking.py
│   │   ├── maintenance.py
│   │   └── common.py
│   ├── schemas/               # Pydantic schemas (Request/Response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── inventory.py
│   │   ├── booking.py
│   │   └── maintenance.py
│   ├── crud/                  # Database CRUD operations
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── inventory.py
│   │   └── booking.py
│   ├── api/                   # Routers (endpoints)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── inventory.py
│   │   ├── booking.py
│   │   └── auth.py
│   ├── auth/                  # JWT auth utils
│   │   ├── __init__.py
│   │   ├── auth_handler.py    # JWT encode/decode
│   │   └── dependencies.py    # Current user / role checking
│   ├── db/                    # DB session management
│   │   ├── __init__.py
│   │   └── database.py
│   ├── utils/                 # Helper functions
│   │   ├── __init__.py
│   │   ├── scheduler.py       # Conflict resolution
│   │   ├── alerts.py          # Low stock / expiry notifications
│   │   └── analytics.py       # Predictive analysis engine
│   └── tasks/                 # Background tasks (optional: Celery)
│       └── task_worker.py
│
├── alembic/                  # DB migrations (alembic init here)
│
├── .env                      # Env vars (DB_URL, JWT_SECRET, etc.)
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker config
├── docker-compose.yml        # DB + App services
└── README.md
```