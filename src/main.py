from typing import Optional
from fastapi import FastAPI
from joblib import load
import pandas as pd
from sklearn.metrics import mean_squared_error as mse
import nltk
from src.Limpieza import Limpieza

app = FastAPI()

@app.post("/predict")
def make_predictions(LdataModel:list):

   rta={}
   model = load("assets/vectorizador.joblib")
 
   df = pd.DataFrame(LdataModel)
   df['text'] = df['text'].apply(Limpieza)
   result = model.predict(df['text']) 

   aux=result.tolist()

   for x in range(0,len(aux)):
      if aux[x]== 0:
         rta["text-"+str(x)]="non-suicide"
      else:
         rta["text-"+str(x)]="suicide"
   return rta


