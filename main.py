from fastapi import FastAPI
from app.database import init_db
from app.routes import router

# Initialize App
app = FastAPI(
    title="LogicGate Enterprise",
    version="3.0.0",
    description="A secured, structured microservice."
)

# Startup Tasks
@app.on_event("startup")
def on_startup():
    init_db()

# Connect the Router
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"system": "LogicGate Enterprise Online", "docs": "/docs"}