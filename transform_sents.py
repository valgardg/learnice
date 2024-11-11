transformed = []

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

print(transformed[2])

print(len(transformed))