import spacy

trained_nlp = spacy.load("models/output/model-best")
text = "Milady is a collection on Facebook"
doc = trained_nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)