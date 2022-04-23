import spacy

# trained_nlp = spacy.load("models/output/model-best")
nlp = spacy.load('en_core_web_sm')



def multi_run_ner(args):
   return get_ner_data(*args)

def get_ner_data(text):
    entities = []
    doc = nlp(text)
    for ent in doc.ents:
        entities.append(ent.label_)
    return entities

