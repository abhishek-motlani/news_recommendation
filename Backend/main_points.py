from fastapi import FastAPI
from main_application_endpoints import router1
from dashboard_endpoints import router2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; update for production (e.g., frontend URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Include both routers
app.include_router(router1)
app.include_router(router2)
