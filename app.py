import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#The batch prediction pipeline uses FastAPI and Jinja2 templates to process uploaded CSV files and display predictions in the FastAPi.
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict") #batch prediction, this decorator indicates that this function will handle POST requests to the /predict endpoint.
async def predict_route(request: Request,file: UploadFile = File(...)): #The function accepts a file upload via the UploadFile parameter.
    try:
        df=pd.read_csv(file.file)
        #print(df)

        #loading the preprocessor and model object
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)

        print(df.iloc[0]) #printing first row of dataframe

        y_pred = network_model.predict(df) #making predictions using the loaded model
        print(y_pred)
        df['predicted_column'] = y_pred #adding predictions to dataframe
        print(df['predicted_column']) #printing the predicted column

        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()

        df.to_csv('prediction_output/output.csv') #saving the dataframe with predictions to a CSV file 
        table_html = df.to_html(classes='table table-striped') #converting the dataframe to an HTML table format
        #print(table_html)
         #rendering the HTML table using a Jinja2 template and returning it as the response
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
