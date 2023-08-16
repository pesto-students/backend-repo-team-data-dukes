from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from urls.urls import mount_urls
from handlers.exception import mount_exception_handler

app = FastAPI()
api_v1_router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

api_v1_router = mount_urls(api_v1_router)
app = mount_exception_handler(app)
app.include_router(api_v1_router, prefix="/api/v1")

