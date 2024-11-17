from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tag_sentence import predict_tags
from translate_word import translate_english_to_icelandic
from classify_sentence import classify_sentence_language

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List the frontend URL(s) allowed to access this backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/tag/{sentence}")
def pos_tag_sentence(sentence: str):
    sentence_lang = classify_sentence_language(sentence)
    if sentence_lang == "English-Latin1":
        translated_icelandic_sentence = translate_english_to_icelandic(sentence)
        tagged_sentence = predict_tags(translated_icelandic_sentence)
    else:
        tagged_sentence = predict_tags(sentence)
    return tagged_sentence


@app.get("/tag/english/{sentence}")
def pos_tag_englsih(sentence: str):
    translated_icelandic_sentence = translate_english_to_icelandic(sentence)
    tagged_sentence = predict_tags(translated_icelandic_sentence)
    return tagged_sentence