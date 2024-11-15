from transformers import BertTokenizer, BertForTokenClassification
from transformers import pipeline

# Load pre-trained mBERT model and tokenizer
model_name = "bert-base-multilingual-cased"
model = BertForTokenClassification.from_pretrained(model_name, num_labels=17)  # 17 is an example for PoS classes, adjust if needed
tokenizer = BertTokenizer.from_pretrained(model_name)

# Set up the pipeline for token classification (PoS tagging)
pos_tagger = pipeline("ner", model=model, tokenizer=tokenizer)

# Example Icelandic sentence
sentence = "Ég fer í skóla"  # "I go to school"

# Run the pipeline
results = pos_tagger(sentence)
print(results)
