# Load the fine-tuned model
from transformers import BertTokenizerFast, BertForTokenClassification
import torch
import json

# Load id2tag mapping
with open("id2tag_testing.json", "r") as f:
    id2tag = json.load(f)

print(id2tag["0"])

# Load your tokenizer and model from saved checkpoint
tokenizer = BertTokenizerFast.from_pretrained("./fine_tuned_bert_icelandic_testing")
model = BertForTokenClassification.from_pretrained("./fine_tuned_bert_icelandic_testing")

# Function to predict tags on a new sentence
def predict_tags(sentence, tokenizer, model, id2tag):
    # Tokenize the sentence
    tokenized_input = tokenizer(sentence, is_split_into_words=True, return_tensors="pt")
    
    # Get predictions
    with torch.no_grad():
        output = model(**tokenized_input)
    
    # Get predicted label IDs
    label_ids = torch.argmax(output.logits, dim=2).squeeze().tolist()

    # Convert label IDs to tag names
    print(f'Og label_ids: {label_ids}')
    tags = [id2tag[str(label_id)] if str(label_id) in id2tag else 'O' for label_id in label_ids]
    print(f'generated tags: {tags}')
    # Filter out predictions for padding tokens
    word_ids = tokenized_input.word_ids()  # Match back to original words
    tags = [tag for tag, word_id in zip(tags, word_ids) if word_id is not None]
    
    # Return the tokens and their corresponding tags
    return list(zip(sentence, tags))

# Example usage with a new Icelandic sentence
sentence = ["Hraunbær", "105", "."]
predicted_tags = predict_tags(sentence, tokenizer, model, id2tag)

print("Predicted Tags:", predicted_tags)