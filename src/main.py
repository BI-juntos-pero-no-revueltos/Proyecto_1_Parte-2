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
from Limpieza import Limpieza
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
   model = load("vectorizador.joblib")
 
   '''
   i=1
   for x in LdataModel:
      df = pd.DataFrame(x, columns=x.keys(), index=[0])

      df['text'] = df['text'].apply(Limpieza)

      result = model.predict(df)
      rta[i]=result[0]
      i+=1   
   '''   
   df = pd.DataFrame(LdataModel)
   print(df)
   df['text'] = df['text'].apply(Limpieza)
   print(df)
   result = model.predict(df['text']) 
   print(result)
 
   return rta


