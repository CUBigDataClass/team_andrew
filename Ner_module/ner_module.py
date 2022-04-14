import spacy

# trained_nlp = spacy.load("models/output/model-best")
nlp = spacy.load('en_core_web_sm')


def multi_run_ner(args):

   return get_ner_data(*args)


def get_ner_data(text,id):
    out = {}
    entities = []
    doc = nlp(text)
    for ent in doc.ents:
        entities.append({'_id':id,'Word':ent.text,"Entity":ent.label_})
    out["ner_vals"] = entities
    return out

print(get_ner_data("Microsoft is a big company",7888))