import torch
from torch.utils.data import Dataset
from transformers import BertTokenizerFast
import nltk
from nltk import FreqDist

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

# load mBERT tokenizer
tokenizer = BertTokenizerFast.from_pretrained('bert-base-multilingual-cased')

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

