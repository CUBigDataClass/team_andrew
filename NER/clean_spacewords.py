# pip install --user -U pip setuptools wheel
# pip install --user -U spacy

# !pip install --user pyresparser
# !pip install --user spacytextblob
# !python -m textblob.download_corpora
# !python -m spacy download en_core_web_sm

import spacy
import string

def removeSW(phrase):
    new_string = phrase.translate(str.maketrans('', '', string.punctuation))

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(new_string)
    
    holderArr = []
    for token in doc:
        if (token.is_stop == False and token.text != ' '):
            holderArr.append(token.text.lower())


    return holderArr

print(removeSW("Best dog breeds for first-time owners: 5 easy to train pups | HELLO!"))
print(removeSW("10 Cutest Dog Breeds"))
print(removeSW("The 10 Cutest Dog Breeds! (2022) - We Love Doodles"))
print(removeSW("15 Cute Dog Breeds You Won't Be Able To Resist | Southern Living"))
print(removeSW("43 Best Small Dog Breeds - Toy Breed Dogs"))
    