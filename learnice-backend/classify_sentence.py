import joblib
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

model_filename = 'ice_eng_classifier.pkl'
loaded_pipeline = joblib.load(model_filename)
print("Model loaded successfully")

def classify_sentence_language(sentence):
    prediction = loaded_pipeline.predict([sentence])
    print(prediction[0])
    return prediction[0]


# classify_sentence('I like playing sports, and did so when I was younger')