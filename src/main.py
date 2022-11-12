from typing import Optional
from fastapi import FastAPI
from joblib import load
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error as mse
import joblib

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

   i=1
   for x in LdataModel:
      df = pd.DataFrame(x, columns=x.keys(), index=[0])
      df.columns = ['text']
      result = model.predict(df)
      rta[i]=result[0]
      i+=1 
   return rta

'''
@app.post("/train")
def train_model(LdataModel:list):
   rta={}
   model = load("assets/modelo.joblib")

   df = pd.DataFrame.from_dict(LdataModel)
   df.columns = ['Serial No.','GRE Score','TOEFL Score','University Rating','SOP',"LOR",'CGPA','Research','Admission Points']
   
   X = df.drop('Admission Points', axis = 1)
   y = df['Admission Points']
   model=model.fit(X,y)

   r2=model.score(X,y)

   y_true = y
   y_predicted = model.predict(X)
   RMSE=np.sqrt(mse(y_true, y_predicted))

   joblib.dump(model,"assets/modelo.joblib")
   return {"R^2": r2, "RMSE": RMSE}
'''