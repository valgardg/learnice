from reynir_correct import check_single

# find any sugguestions or corrections for the given sentence
# sentence is expected to be Icelandic
def check_sentence_grammar(sentence):
    print('checking sentence grammar')
    sent = check_single(sentence)
    grammar_suggestions = []
    for annotation in sent.annotations:
        incorrect  = annotation.original
        corrected = annotation.suggest
        if incorrect != None and corrected != None:
            suggestion = {
                'incorrect': incorrect,
                'corrected': corrected
            }
            grammar_suggestions.append(suggestion)
    print('returning grammar_suggestoins')
    return grammar_suggestions