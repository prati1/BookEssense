from fastapi import FastAPI
from app.api.routes import user as user_routes
from app.api.routes import auth as auth_routes
from app.api.routes import analysis as analysis_routes
from app.db.base import Base, engine
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = settings.secret_key or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth_routes.router, tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(analysis_routes.router, prefix="/analysis", tags=["analysis"])
