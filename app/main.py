# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import reorder
from app.api import user, inventory, booking, auth
from app.db.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Inventory Management System",
    description="An intelligent platform to manage school resources and inventory.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- This is set to "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(booking.router, prefix="/bookings", tags=["Bookings"])
app.include_router(reorder.router, tags=["Prediction"])

# Health check
@app.get("/")
def root():
    return {"message": "Welcome to the School Inventory Management API"}
