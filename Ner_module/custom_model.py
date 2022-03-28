import spacy

trained_nlp = spacy.load("models/output/model-best")
text = "We love microsoft"
doc = trained_nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)