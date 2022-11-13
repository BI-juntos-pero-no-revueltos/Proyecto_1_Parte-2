from typing import Optional
from fastapi import FastAPI
from joblib import load
import pandas as pd
from sklearn.metrics import mean_squared_error as mse
import re
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

app = FastAPI()

@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_predictions(LdataModel:list):

   rta={}
   model = load("assets/modelo.joblib")
   '''
   i=1
   for x in LdataModel:
      df = pd.DataFrame(x, columns=x.keys(), index=[0])
      df.columns = ['text']

      df = transform(df)

      result = model.predict(df)
      rta[i]=result[0]
      i+=1       
   '''
   df = pd.DataFrame(LdataModel)
   df.columns = ['text']
   print(df)
   df = transform(df['text'])

   

   result = model.predict(df)
   
   rta[0]=result[0]
   rta[1]=result[1]
   return rta


def transform(X):
   documents = []
   stemmer = WordNetLemmatizer()

   for sen in range(0, len(X)):
      # Remove all the special characters
      document = re.sub(r'\W', ' ', str(X[sen]))
      
      # remove all single characters
      document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
      
      # Remove single characters from the start
      document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
      
      # Substituting multiple spaces with single space
      document = re.sub(r'\s+', ' ', document, flags=re.I)
      
      # Removing prefixed 'b'
      document = re.sub(r'^b\s+', '', document)
      
      # Converting to Lowercase
      document = document.lower()
      
      # Lemmatization
      document = document.split(' ')

      document = [stemmer.lemmatize(word) for word in document]
      document = ' '.join(document)
      
      documents.append(document)
   
   vectorizer = CountVectorizer(stop_words=stopwords.words('english'))
   X = vectorizer.fit_transform(documents).toarray()
   tfidfconverter = TfidfTransformer()
   X = tfidfconverter.fit_transform(X).toarray()

   return X