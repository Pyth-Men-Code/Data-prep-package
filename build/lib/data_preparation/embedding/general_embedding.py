# Fonction de prétraitement pour exclure les mots non anglais et les mots vides

from curses.ascii import isalpha
import nltk
from nltk.corpus import words, stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import string
import emoji

# Téléchargement de la liste des mots anglais si nécessaire
nltk.download('words')
nltk.download('stopwords')
english_words = set(words.words())
stopwords = nltk.corpus.stopwords.words("english") 
lemmatizer = WordNetLemmatizer()

# remouve stop_words
def remove_stopwords(tokens):
    return [token for token in tokens if token not in stopwords]

# keep english words only
def english_only(text):
    return ' '.join([word for word in text.split() if word.lower() in english_words])

# remouve spaces and noise 
def wordopt(text):
    text = text.lower()
    # suppression des expression entre crochets
    text = re.sub('\[.*?]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    #text = re.sub(r'\s+', '', text)
    text = re.sub('\w*\d\w*', '', text)
    # remouve speciale caractere
    text = re.sub('&gt;', '>', text)
    text = re.sub('&lt;', '<', text)
    text = re.sub('&quot;', '\"', text)
    text = re.sub('&amp;', '&', text)
    # suppression des tags(@soso1234)
    text = re.sub('@/s+', '', text)
    # Remplacer les mentions @XXX par ' user '
    text = re.sub(r"^@\S+|\s@\S+", 'user_net', text)
    # Remplacer les #XXX par ' hashtags 
    text = re.sub(r"^#\S+|\s#\S+", ' hashtag ', text)
    # lemmatization
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

# remplacer les emoticon 
def remp_emoticon(text):  # Remplacer les emoticones par leur signification
    import re
    # mettre \ devant : ) ^
    # pas de \ devant : ; : - ] >
    text = re.sub(
        ';p|;P|:p|:P|xp|xP|=p|=P|:‑P|X‑P|x‑p|:‑p|:‑Þ|:‑þ|:‑b|>:P|d:|:b|:þ|:Þ',
        ' emoticon_langue ', text)
    text = re.sub(':"D', 'emoticon_joyeux', text)
    text = re.sub(
        ":‑\)|:\)|:-]|:]|:->|:>|8-\)|8\)|:-}|:}|:o\)|:c\)|:\^\)|=]|=\)|:-\)\)|:'‑\)|:'\)",
        ' emoticon_joyeux ',    text)
    text = re.sub(':‑D|:D|8‑D|8D|=D|=3|B\^D|c:|C:|x‑D|xD|X‑D|XD',
                      ' emoticon_rire ',    text)
    text = re.sub(
        ":‑\(|:\(|:‑c|:c|:‑<|:<|:‑\[|:\[|>:\[|:{|:@|:\(|;\(|:'‑\(|:'\(|:=\(|v.v",
        ' emoticon_triste ',    text)
    text = re.sub("D‑':|D:<|D:|D8|D;|D=|DX", ' emoticon_degout ',   text)
    text = re.sub(
        ":‑O|:O|:‑o|:o|:-0|8‑0|>:O|=O|=o|=0|O_O|o_o|O-O|o‑o|O_o|o_O",
        ' emoticon_surprise ',  text)
    text = re.sub(":-3|:3|=3|x3|X3|>:3", ' emoticon_chat ', text)
    text = re.sub(":-\*|:\*|:×|<3", ' emoticon_amour ', text)
    text = re.sub(";‑\)|;\)|\*-\)|\*\)|;‑]|;]|;\^\)|;>|:‑,|;D|;3|:‑J",
                      ' emoticon_clindoeil ',   text)
    text = re.sub(":-/ |>.<|>_<|:/|:‑.|>:\|>:/|:\|=/|=\|:L|=L|:S",
                      ' emoticon_sceptique ',   text)
    text = re.sub(
        "<_<|>_>|<.<|>.>|:$|://|://3|:‑X|:X|:‑#|:#|:‑&|:&|%‑\)|%\)",
        ' emoticon_embarrasse ',    text)
    text = re.sub("8-X|8=X|x-3|x=3|X_X|x_x", ' emoticon_mort ', text)

    return  text

# Remplacer les abréviations
def remp_abreviation(text):  
    # specific
    text = text.lower()
    text = re.sub("won\'t", "will not", text)
    text = re.sub("can\'t", "can not", text)
    text = re.sub("cannot", "can not", text)
    text = re.sub("didnt", "did not", text)
    text = re.sub("couldnt", "could not", text)
    text = re.sub("doesnt", "does not", text)
    text = re.sub("dont", "do not", text)
    text = re.sub("hasnt", "has not", text)
    text = re.sub("hadnt", "had not", text)
    text = re.sub("havent", "have not", text)
    text = re.sub("ive", "i have", text)
    text = re.sub("im", "i am", text)
    text = re.sub("wasnt", "was not", text)
    text = re.sub("werent", "were not", text)
    text = re.sub("'cause", "because", text)
    text = re.sub("cos", "because", text)
    text = re.sub("f\*\*k", "fuck", text)
    text = re.sub("f\*\*king", "fucking", text)
    text = re.sub("idk", "i do not know", text)
    # general
    text = re.sub("n\'t", " not", text)
    text = re.sub("n\'", " not", text)
    text = re.sub("' re", " are", text)
    text = re.sub("\'s", " is", text)
    text = re.sub("\'d", " would", text)
    text = re.sub("\'ll", " will", text)
    text = re.sub("\'t", " not", text)
    text = re.sub("\'ve", " have", text)
    text = re.sub(" m", " am ", text)
    text = re.sub(" u ", " you ", text)
    text = re.sub(" ur ", " your ", text)
    text = re.sub(" n ", " and ", text)

    return text

# remouve emojis
def remove_emoji(text) : 
    # Convert emojis to their corresponding names or aliases
    text_without_emojis = emoji.demojize(text)
    # Remove emojis (text between colons)
    text_without_emojis = ''.join(word for word in text_without_emojis.split(':') if not any(char.isdigit() for char in word))
    return text_without_emojis

# remove sigle lettre like ['A','Y'......]
def remove_single_lettre(text) : 
    text = " ".join(
        v for v in text.split if ((len(v>1) or (not v.isalpha())))
        )
    return text              

# Fonction pour retourner l'étiquette prédite
def output_label(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Not A Fake News"


# fonction pour nettoyer et vectorizer le text
def manual_testing(news):
    vectorizer = TfidfVectorizer()
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorizer.fit_transform(new_x_test)
    pred_KNN = model.predict(new_xv_test)
    return output_label(pred_KNN[0])

# Tf-idf vectorization
def text_vectorization(data, col, size):  # data=input data, col=colonne text, size=nombre de mots à considerer

    tfidf_vect = TfidfVectorizer(max_features=size, preprocessor=english_only, stop_words='english', min_df=1)
    X = tfidf_vect.fit_transform(data[col])
    data_text = pd.DataFrame(X.toarray())
    data_text.columns = tfidf_vect.get_feature_names_out()  # names_out
    data[data_text.columns] = data_text
    data = data.drop(columns=col)
    return data