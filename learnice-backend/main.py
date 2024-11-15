from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tag_sentence import predict_tags

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # List the frontend URL(s) allowed to access this backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/tag/{sentence}")
def pos_tag_sentence(sentence: str):
    tagged_sentence = predict_tags(sentence)
    return tagged_sentence