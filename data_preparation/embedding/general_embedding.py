# Fonction de prétraitement pour exclure les mots non anglais et les mots vides

import nltk
from nltk.corpus import words
from sklearn.feature_extraction.text import TfidfVectorizer

# Téléchargement de la liste des mots anglais si nécessaire
nltk.download('words')
english_words = set(words.words())

# Fonction de prétraitement pour exclure les mots non anglais et les mots vides
def english_only(text):
    return ' '.join([word for word in text.split() if word.lower() in english_words])

def text_vectorization(data,col,size): #data=input data, col=colonne text, size=nombre de mots à considerer

    tfidf_vect = TfidfVectorizer(max_features=size,preprocessor=english_only, stop_words='english',min_df=1)
    X = tfidf_vect.fit_transform(data[col])
    data_text = pd.DataFrame(X.toarray())
    data_text.columns = tfidf_vect.get_feature_names_out()  #names_out
    data[data_text.columns]=data_text
    data = data.drop(columns=col)
    return data