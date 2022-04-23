import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk
import unidecode
from collections import Counter


lemmatizer = nltk.stem.WordNetLemmatizer()
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
stop = set(stopwords.words('english'))

def text_preprocessing(text):
    # Replacing all the occurrences of \n,\\n,\t,\\ with a space.
    text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t', ' ').replace('\\', ' ').replace('. com', '.com')
    # strip html tags
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")
    # remove links
    stripped_text = re.sub(r'http\S+', '', stripped_text)
    stripped_text = re.sub(r"\ [A-Za-z]*\.com", " ", stripped_text)
    # remove whitespace
    pattern = re.compile(r'\s+')
    no_whitespace = re.sub(pattern, ' ', stripped_text)
    stripped_text = no_whitespace.replace('?', ' ? ').replace(')', ') ')
    # Removing unicode characters
    stripped_text = unidecode.unidecode(stripped_text)
    # Changing words like cherrrrrrrry to cherry
    pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
    stripped_text = pattern_alpha.sub(r"\1\1", stripped_text)
    pattern_punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')
    stripped_text = pattern_punct.sub(r'\1', stripped_text)
    stripped_text = re.sub(' {2,}', ' ', stripped_text)

    # tokens = stripped_text.split(' ')
    # for word in tokens:
    #     if word in cont_map:
    #         tokens = [item.replace(word, cont_map[word]) for item in tokens]

    # text = ' '.join(str(e) for e in tokens)
    # removing special characters and numbers
    text = re.sub('[^A-Za-z0-9]+', ' ', stripped_text)
    text = re.sub(r"[^a-zA-Z:$-,%.?!]+", ' ', text)
    # lemmatization swimming , swim
    text = [lemmatizer.lemmatize(w, 'v') for w in w_tokenizer.tokenize(text)]
    # removing stopwords
    text = ' '.join([word for word in text if word not in stop])
    return text


def get_top_words(text,top_words=5):
    stop = set(stopwords.words('english'))
    corpus = [word for i in text for word in i]
    corpus = [word for word in corpus if word not in stop]
    counter = Counter(corpus)
    most = counter.most_common()
    x = []
    for word, count in most[:top_words]:
        if (word not in stop):
            x.append(word)
    return x

def check_top_ents(top_ents):
    if len(top_ents) < 1:
        return top_ents.extend(["NFT","NFT","NFT"])
    elif len(top_ents) < 2:
        return top_ents.extend(["NFT","NFT"])
    elif len(top_ents) < 3:
        return top_ents.append(["NFT"])
    else:
        return top_ents