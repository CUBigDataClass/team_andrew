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
        if (token.is_stop == False):
            holderArr.append(token.text)
        
    return holderArr

print(removeSW("Tommorow will be too late, its now or never."))
    