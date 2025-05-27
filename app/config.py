# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from `.env` file
load_dotenv()

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_SECONDS = int(os.getenv("JWT_EXPIRE_SECONDS", 3600))

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/school_inventory")

# Other optional settings
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
