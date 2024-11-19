from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List

from check_grammar import check_sentence_grammar
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
    """
    Perform POS tagging and grammar checking for a given sentence.
    If the sentence is in English, translate it to Icelandic before processing.
    """
    try:
        # Step 1: Detect the sentence language
        sentence_lang = classify_sentence_language(sentence)

        # Step 2: Translate if needed and process the sentence
        if sentence_lang == "English-Latin1":
            translated_icelandic_sentence = translate_english_to_icelandic(sentence)
            tagged_sentence = predict_tags(translated_icelandic_sentence)
            grammar_suggestions = [] # assume that translation doesn't contain spelling or grammar mistakes
        else:
            tagged_sentence = predict_tags(sentence)
            grammar_suggestions = check_sentence_grammar(sentence)

        # Step 3: Prepare the response
        return {
            "tagged-sentence": tagged_sentence,  # Tagged sentence structure
            "suggestions": grammar_suggestions,  # Grammar suggestions
            "predicted-language": sentence_lang  # Detected language
        }
    except Exception as e:
        # Handle unexpected errors gracefully
        return {"error": str(e)}