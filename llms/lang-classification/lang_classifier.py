import joblib
import random
import nltk
from nltk.corpus import udhr
from sklearn.utils import shuffle
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('udhr')

def train_udhr(pipeline):
    X = []
    y = []

    for lang in languages:
        words = udhr.words(lang)
        sents = [" ".join(random.choices(words, k=random.randint(3,18))) for x in range(5000)]
        X.extend(sents)
        y += [lang] * len(sents)
    
    X, y = shuffle(X, y, random_state=42)
    X_train, X_test, y_train, y_test, = train_test_split(X, y, test_size=0.1, random_state=42)

    pipeline.fit(X_train, y_train)
    return X_test, y_test

languages = ['Icelandic_Yslenska-Latin1', 'English-Latin1']

q1_pipeline = Pipeline([
    ('vect', CountVectorizer(ngram_range=(1,3), analyzer='char')),
    ('clf', LogisticRegression(solver='liblinear'))
])

X_test, y_test = train_udhr(pipeline=q1_pipeline)
score = q1_pipeline.score(X_test, y_test)
print("Accuracy: {:.1%}".format(score))

model_filename = 'ice_eng_classifier.pkl'
joblib.dump(q1_pipeline, model_filename)
print(f'Model saved to {model_filename}')