from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.user import router as user_router
from routers.login import router as login_router
from routers.basic_login import router as basic_login_router
from db.client import engine, Base
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# ✅ CORS MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",      # Live Server
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:5500",      # Alternative localhost
        "*"                            # Allow all origins (development)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")
except Exception as e:
    print(f"❌ Table creation failed: {e}")

# Include API routers
app.include_router(user_router)
app.include_router(login_router)
app.include_router(basic_login_router)

# ✅ MOUNT FRONTEND - Corrected path
# Current location: Backend/FastAPI/main.py
# Need to reach: frontend/ (at LATEST_PROJECT/frontend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Backend/FastAPI/
PARENT_DIR = os.path.dirname(BASE_DIR)                 # Backend/
PROJECT_ROOT = os.path.dirname(PARENT_DIR)             # LATEST_PROJECT/
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")  # LATEST_PROJECT/frontend/

print(f"\n📍 Current file: {os.path.abspath(__file__)}")
print(f"📍 Backend dir: {BASE_DIR}")
print(f"📍 Project root: {PROJECT_ROOT}")
print(f"📍 Frontend dir: {FRONTEND_DIR}")
print(f"📍 Frontend exists: {os.path.exists(FRONTEND_DIR)}\n")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    print("✅ Frontend mounted successfully at /")
    print("📌 Access: http://localhost:8000/index.html")
    print("📌 Access: http://localhost:8000/login.html")
    print("📌 Access: http://localhost:8000/home.html\n")
else:
    print(f"❌ Frontend directory not found at {FRONTEND_DIR}\n")
    print(f"   Checked path: {os.path.abspath(FRONTEND_DIR)}\n")

@app.get("/api/status")
async def status():
    return {"message": "Backend is running!", "status": "ok"}

# Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000