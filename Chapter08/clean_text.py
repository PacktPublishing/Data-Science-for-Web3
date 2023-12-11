import re
import unidecode
import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

tok = WordPunctTokenizer()
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


pat1 = r'https[^ ]+'
pat2 = r'www.[^ ]+'
pat = r'|'.join((pat1, pat2))
filter = ['crypto', 'bitcoin', 'ethereum', 'company', 'blockchain', 'say', 'million']


def get_clean_text(text):
    text = str(text)
    text = text.lower()
    text = unidecode.unidecode(text)
    text = re.sub(pat, ' ', text)
    text = [w for w in tok.tokenize(text) if w not in stop_words]
    text = [w for w in text if len(w) > 3]
    text = [wordnet_lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in text]
    text = [w for w in text if w not in filter]
    text = (' '.join(text)).strip()
    return text
