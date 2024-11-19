# Load the fine-tuned model
from transformers import BertTokenizerFast, BertForTokenClassification
import torch # type: ignore
import json
import math
from collections import defaultdict

def read_lines_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

# Load id2tag mapping
with open("../models/ftbi_ds100/id2tag_ftbi_ds100.json", "r") as f:
    id2tag = json.load(f)

# Load your tokenizer and model from saved checkpoint
tokenizer = BertTokenizerFast.from_pretrained("../models/ftbi_ds100")
model = BertForTokenClassification.from_pretrained("../models/ftbi_ds100")

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
    
    return word_tags

def separate_sentence_and_tags(line):
    """
    Separates a line of text into a sentence without tags and a list of tags.

    Args:
        line (str): Input line where each token is formatted as 'word/tag'.

    Returns:
        tuple: A tuple containing:
            - sentence (str): The sentence without tags.
            - tags (list): A list of tags extracted from the line.
    """
    words = []
    tags = []
    # Split the line into tokens by whitespace
    tokens = line.split()
    for token in tokens:
        if '/' in token:
            word, tag = token.rsplit('/', 1)  # Use rsplit to handle words with slashes
            words.append(word)
            tags.append(tag)
        else:
            words.append(token)  # Add token as-is if it doesn't contain a tag
    
    # Join the words into a sentence
    sentence = ' '.join(words)
    return sentence, tags

def calculate_metrics(lines, tokenizer, model, id2tag):
    correct = 0
    total = 0
    true_positive = defaultdict(int)
    false_positive = defaultdict(int)
    false_negative = defaultdict(int)

    # Read and process each line
    for i in range(len(lines)):
        line = lines[i]
        print(f'line {i} of {len(lines)}')
        # Separate sentence and true tags
        sentence, true_tags = separate_sentence_and_tags(line)

        # Get predicted tags
        predicted_tags = predict_tags(sentence.split(), tokenizer, model, id2tag)

        # Compare true and predicted tags
        for true_tag, predicted_tag in zip(true_tags, predicted_tags):
            total += 1
            if true_tag == predicted_tag:
                correct += 1
                true_positive[true_tag] += 1
            else:
                false_positive[predicted_tag] += 1
                false_negative[true_tag] += 1

    # Calculate metrics
    accuracy = correct / total if total > 0 else 0

    precision = {tag: true_positive[tag] / (true_positive[tag] + false_positive[tag])
                 if (true_positive[tag] + false_positive[tag]) > 0 else 0
                 for tag in true_positive}
    recall = {tag: true_positive[tag] / (true_positive[tag] + false_negative[tag])
              if (true_positive[tag] + false_negative[tag]) > 0 else 0
              for tag in true_positive}

    macro_precision = sum(precision.values()) / len(precision) if precision else 0
    macro_recall = sum(recall.values()) / len(recall) if recall else 0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall
    }

# Example usage with a new Icelandic sentence
# sentence = ["Hraunbær", "105", "."]
# sentence = ["Niðurstaða", "þess", "var", "neikvæð", "."]
# sentence = "Kl. 9-16 fótaaðgerðir og hárgreiðsla , Kl. 9.15 handavinna , Kl. 13.30 sungið við flygilinn , Kl. 14.30-16 dansað við lagaval Halldóru , kaffiveitingar allir velkomnir .".split()
lines = read_lines_from_file('../data/MIM-GOLD.sent')
# predicted_tags = predict_tags(lines[0].split(), tokenizer, model, id2tag)

metrics = calculate_metrics(lines[:math.ceil(0.1 * len(lines))], tokenizer, model, id2tag)

print("Accuracy:", metrics["accuracy"])
print("Macro Precision:", metrics["macro_precision"])
print("Macro Recall:", metrics["macro_recall"])
# print("Per-tag Precision:", metrics["precision"])
# print("Per-tag Recall:", metrics["recall"])