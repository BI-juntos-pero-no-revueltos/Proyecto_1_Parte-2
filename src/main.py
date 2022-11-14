from typing import Optional
from fastapi import FastAPI
from joblib import load
import pandas as pd
from sklearn.metrics import mean_squared_error as mse
import nltk
from src.Limpieza import Limpieza

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
   model = load("assets/vectorizador.joblib")
 
   df = pd.DataFrame(LdataModel)
   df['text'] = df['text'].apply(Limpieza)
   result = model.predict(df['text']) 

   aux=result.tolist()

   for x in range(0,len(aux)):
      rta["text-"+str(x)]=aux[x]

   return rta


