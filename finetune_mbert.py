import torch
from torch.utils.data import Dataset
from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# load mBERT tokenizer
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

# testing
# tokenized_input, aligned_tags = align_tags_with_tokens(['Fræðslu-', 'og', 'kynningarfundur', 'kl.', '14', '.'], ['kt', 'c', 'nken', 'ks', 'ta', 'pl'], tokenizer)
# print(f'tokenized_input: {tokenized_input}\naligned_tags: {aligned_tags}')

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
    
dataset = PosDataset(data=transformed, tokenizer=tokenizer, max_length=128)

# Load BERT model for token classification
model = BertForTokenClassification.from_pretrained("bert-base-multilingual-cased", num_labels=len(tag2id))

# Define the metrics for evaluation
def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=2)

    # Mask out padding tokens (-100) when computing metrics
    mask = labels != -100
    labels = labels[mask]
    preds = preds[mask]

    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="weighted")
    accuracy = accuracy_score(labels, preds)

    return {
        "accuracy": accuracy,
        "f1": f1,
        "precision": precision,
        "recall": recall
    }

# Set up Trainer and TrainingArguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=16,
    gradient_accumulation_steps=2,
    per_device_eval_batch_size=16,
    eval_accumulation_steps=4, # internet says this could help with evaluation memory issues; processes evaluation batches in small chuncks instead of all at once
    num_train_epochs=3,
    weight_decay=0.01,
    fp16=True, # added fp16 as it can lead to better memory management at close to no cost of performance (supposedly)
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,  # Use a train/validation split in practice
    eval_dataset=dataset,   # Use separate validation dataset in practice
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model and tokenizer
model.save_pretrained("./fine_tuned_bert_icelandic")
tokenizer.save_pretrained("./fine_tuned_bert_icelandic")