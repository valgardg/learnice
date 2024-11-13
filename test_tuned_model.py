# Load the fine-tuned model
from transformers import BertTokenizerFast, BertForTokenClassification
import torch
import json

# Load id2tag mapping
with open("./fine_tuned_bert_icelandic_label_testing/id2tag_testing.json", "r") as f:
    id2tag = json.load(f)

# Load your tokenizer and model from saved checkpoint
tokenizer = BertTokenizerFast.from_pretrained("./fine_tuned_bert_icelandic_label_testing")
model = BertForTokenClassification.from_pretrained("./fine_tuned_bert_icelandic_label_testing")

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
    tags = [id2tag[str(label_id)] if str(label_id) in id2tag else 'O' for label_id in label_ids]
    
    # Match back to original words
    word_ids = tokenized_input.word_ids()  # This shows which original word each token corresponds to
    word_tags = []
    current_word_id = None
    current_tags = []

    # Aggregate tags for each word
    for word_id, tag in zip(word_ids, tags):
        if word_id is None:  # Skip special tokens
            continue
        if word_id != current_word_id:  # New word detected
            if current_tags:  # Append the aggregated tag for the previous word
                word_tags.append(current_tags[0])  # Use the first tag, or customize this
            current_word_id = word_id
            current_tags = [tag]
        else:
            current_tags.append(tag)  # Aggregate tags for the same word

    # Append the last word's tag
    if current_tags:
        word_tags.append(current_tags[0])  # Use the first tag, or customize this
    
    # Return the original words and their aggregated tags
    return list(zip(sentence, word_tags))

# Example usage with a new Icelandic sentence
sentence = ["Hraunbær", "105", "."]
sentence = ["Niðurstaða", "þess", "var", "neikvæð", "."]
sentence = "Kl. 9-16 fótaaðgerðir og hárgreiðsla , Kl. 9.15 handavinna , Kl. 13.30 sungið við flygilinn , Kl. 14.30-16 dansað við lagaval Halldóru , kaffiveitingar allir velkomnir .".split()
predicted_tags = predict_tags(sentence, tokenizer, model, id2tag)

print("Predicted Tags:", predicted_tags)