from reynir_correct import check_errors

# Icelandic sentence to check
sentence = "Ég er að skrifa eitthvað rangt málfræði."

# Perform grammar checking
corrections = check_errors(sentence)

# Display results
if corrections:
    print("Errors detected:")
    for error in corrections:
        print(f"- {error['text']}")
else:
    print("No errors found.")