# Fonction de prétraitement pour exclure les mots non anglais et les mots vides

import nltk
from nltk.corpus import words, stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import string

# Téléchargement de la liste des mots anglais si nécessaire
nltk.download('words')
nltk.download('stopwords')
english_words = set(words.words())
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


# Fonction de prétraitement pour exclure les mots non anglais et les mots vides
def english_only(text):
    return ' '.join([word for word in text.split() if word.lower() in english_words])


def text_vectorization(data, col, size):  # data=input data, col=colonne text, size=nombre de mots à considerer

    tfidf_vect = TfidfVectorizer(max_features=size, preprocessor=english_only, stop_words='english', min_df=1)
    X = tfidf_vect.fit_transform(data[col])
    data_text = pd.DataFrame(X.toarray())
    data_text.columns = tfidf_vect.get_feature_names_out()  # names_out
    data[data_text.columns] = data_text
    data = data.drop(columns=col)
    return data


def wordopt(text):
    text = text.lower()
    # suppression des expression entre crochets
    text = re.sub('\[.*?]', '', text)
    ext = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub(' +', '', text)
    text = re.sub('\w*\d\w*', '', text)
    # suppression des tags(@soso1234)
    text = re.sub('@/s+', '', text)
    text = ' '.join([word for word in text.split() if word not in stop_words])
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
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