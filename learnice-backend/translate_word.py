import os
from dotenv import load_dotenv
import boto3

# Load environment variables from the .env file
load_dotenv()

# Get credentials from environment variables
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_DEFAULT_REGION')

# Initialize AWS Translate client using environment variables
translate = boto3.client(
    'translate',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

def translate_icelandic_word_to_english(word):
    translate = boto3.client('translate', region_name='us-east-2')

    try:
        # Call AWS Translate
        response = translate.translate_text(
            Text=word,
            SourceLanguageCode='is',
            TargetLanguageCode='en'
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def translate_english_sentence_to_icelandic(sentence):
    translate = boto3.client('translate', region_name='us-east-2')

    try:
        response = translate.translate_text(
            Text=sentence,
            SourceLanguageCode='en',
            TargetLanguageCode='is'
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
# icelandic_word = "hestur"  # Example Icelandic word
# translated_word = translate_icelandic_to_english(icelandic_word)
# print(f"'{icelandic_word}' in English is: '{translated_word}'")