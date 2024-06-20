from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import router as dog_link_router

app = FastAPI()


origins = [
    "http://127.0.0.1:8888",
    "http://localhost:8888",
    # "http://127.0.0.1:3000",
    # "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dog_link_router)
