import boto3

def translate_icelandic_to_english(word):
    """
    Translates an Icelandic word to English using AWS Translate.

    Parameters:
    word (str): The Icelandic word to translate.

    Returns:
    str: The translated English word.
    """
    # Create a Translate client
    translate = boto3.client('translate', region_name='us-east-2')  # Adjust region if needed

    try:
        # Call AWS Translate
        response = translate.translate_text(
            Text=word,
            SourceLanguageCode='is',  # Icelandic language code
            TargetLanguageCode='en'  # English language code
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def translate_english_to_icelandic(sentence):
    """
    Translates an English sentence to Icelandic using AWS Translate.

    Parameters:
    sentence (str): The English sentence to translate.

    Returns:
    str: The translated Icelandic sentence.
    """
    # Create a Translate client
    translate = boto3.client('translate', region_name='us-east-1')  # Adjust region if needed

    try:
        # Call AWS Translate
        response = translate.translate_text(
            Text=sentence,
            SourceLanguageCode='en',  # English language code
            TargetLanguageCode='is'  # Icelandic language code
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
# icelandic_word = "hestur"  # Example Icelandic word
# translated_word = translate_icelandic_to_english(icelandic_word)
# print(f"'{icelandic_word}' in English is: '{translated_word}'")