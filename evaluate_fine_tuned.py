from transformers import BertTokenizer, BertForTokenClassification
import torch

# Load the fine-tuned model and tokenizer
model = BertForTokenClassification.from_pretrained("./fine_tuned_bert_icelandic")
tokenizer = BertTokenizer.from_pretrained("./fine_tuned_bert_icelandic")

# Define your input sentence
sentence = "opin"

# Tokenize the input sentence
inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)

# Make sure to put the model in evaluation mode
model.eval()

# Perform inference (forward pass)
with torch.no_grad():
    outputs = model(**inputs)

# Get the logits output by the model
logits = outputs.logits

# Apply argmax to get the predicted PoS tags for each token
predicted_ids = torch.argmax(logits, dim=-1)

# Convert token ids back to tag names (use model's label map)
labels = model.config.id2label  # This maps the label indices to human-readable tag labels

# Print the tokens and their predicted PoS tags
tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])  # Get the tokens from input_ids
predicted_tags = [labels[predicted_id.item()] for predicted_id in predicted_ids[0]]

# Print tokens with their predicted tags
for token, tag in zip(tokens, predicted_tags):
    print(f"{token}: {tag}")
