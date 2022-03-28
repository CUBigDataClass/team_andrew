# Load pre-existing spacy model
import spacy
import pandas as pd
from spacy.pipeline import EntityRuler
from collections import defaultdict
import srsly
import typer
import warnings
from pathlib import Path
from spacy.tokens import DocBin

df = pd.read_csv("Opensea_collections.csv")
nlp = spacy.load('en_core_web_sm')
text = []
corpus = []
for i in df['Collections']:
    text.append(str(i) + " is an NFT Collection on Opensea")
for i in text:
    doc = nlp(i)
    for sent in doc.sents:
        corpus.append(sent.text)

# nlp = spacy.blank("en")
ruler = nlp.add_pipe("entity_ruler","ruleActions", config={"overwrite_ents": True})

patterns = []
for i in df['Collections']:
    patterns.append({"label":"NFT","pattern":str(i)})

ruler.add_patterns(patterns)

TRAIN_DATA = []
for sentence in corpus:
    doc = nlp(sentence)
    entities = []

    for ent in doc.ents:
        entities.append([ent.start_char, ent.end_char, ent.label_])
    TRAIN_DATA.append([sentence, {"entities": entities}])
print(TRAIN_DATA[0])


def convert(lang: str, TRAIN_DATA, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

convert("en", TRAIN_DATA, "train.spacy")
convert("en",[['👁 is an NFT Collection on Opensea', {'entities': [[0, 1, 'NFT']]}]], "dev.spacy")