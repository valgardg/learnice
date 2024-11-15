import json
import torch
import math
from torch.utils.data import Dataset
from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

tokenizer = BertTokenizerFast.from_pretrained('bert-base-multilingual-cased')
transformed = []

# turn each line into a sentence tag object
with open('./data/MIM-GOLD.sent', "r") as f:
    for line in f.readlines():
        sentence = []
        tags = []
        tagged_words = line.strip().split(' ')
        for tagged_word in tagged_words:
            tag_and_word = tagged_word.split('/')
            sentence.append(tag_and_word[0])
            tags.append(tag_and_word[1])
        transformed.append({
            "sentence": sentence,
            "tags": tags
        })

unique_tags = list(set(tag for sentence in transformed for tag in sentence["tags"]))
tag2id = {tag: idx for idx, tag in enumerate(unique_tags)}
id2tag = {idx: tag for tag, idx in tag2id.items()}


def align_tags_with_tokens(sentence, tags, tokenizer):
    tokenized_input = tokenizer(sentence, is_split_into_words=True, truncation=True, padding='max_length')
    aligned_tags = []

    word_ids = tokenized_input.word_ids()
    previous_word_idx = None

    for word_idx in word_ids:
        if word_idx is None:
            aligned_tags.append(-100) # Ignore padding tokens
        elif word_idx != previous_word_idx:
            aligned_tags.append(tag2id[tags[word_idx]])
        else:
            aligned_tags.append(-100)
        previous_word_idx = word_idx
    
    return tokenized_input, aligned_tags

class PosDataset(Dataset):
    def __init__(self, data, tokenizer, max_length):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sentence = self.data[idx]["sentence"]
        tags = self.data[idx]["tags"]

        tokenized_input, aligned_tags = align_tags_with_tokens(sentence, tags, self.tokenizer)

        return {
            'input_ids': torch.tensor(tokenized_input['input_ids']),
            'attention_mask': torch.tensor(tokenized_input['attention_mask']),
            'labels': torch.tensor(aligned_tags)
        }
    
eval_dataset = PosDataset(data=transformed[:math.ceil(len(transformed)*0.5)], tokenizer=tokenizer, max_length=128)
print(len(eval_dataset))

def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    accuracy = accuracy_score(labels, preds)
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# Load your tokenizer and model from saved checkpoint
tokenizer = BertTokenizerFast.from_pretrained("./fine_tuned_bert_icelandic_ds50")
model = BertForTokenClassification.from_pretrained("./fine_tuned_bert_icelandic_ds50")

eval_args = TrainingArguments(
    output_dir="./results",
    per_device_eval_batch_size=16,  # Adjust batch size as needed
    logging_dir="./logs",
    report_to="none"  # Disable logging for simplicity in evaluation
)

# Initialize Trainer for evaluation
trainer = Trainer(
    model=model,
    args=eval_args,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
    eval_dataset=eval_dataset
)

# Evaluate the model
results = trainer.evaluate()

# Display evaluation results
print("Evaluation Results:")
for key, value in results.items():
    print(f"{key}: {value}")