import random
import joblib
import nltk
from nltk.corpus import udhr

model_filename = 'ice_eng_classifier.pkl'
loaded_pipeline = joblib.load(model_filename)
print("Model loaded successfully")

# Example sentences to classify
sentences = [
    "Ég er að læra forritun??",  # Icelandic
    "programming",
    "Please tell me this is going to be predicted as an English language, please dear god!",
    "Do you know me!",
    "Why is this wrong."
]

# for sentence, prediction in zip(sentences, predictions):
#     print(f"Sentence: '{sentence}' is classified as: {prediction}")
# languages = ['Icelandic_Yslenska-Latin1', 'English-Latin1']
# for lang in languages:
#     words = udhr.words(lang)
#     sents = [" ".join(random.choices(words, k=random.randint(3,5))) for x in range(1)]
predictions = loaded_pipeline.predict(sentences)

for prediction in predictions:
    print(f'redicted: {prediction}')

# Predict the language for each sentence
