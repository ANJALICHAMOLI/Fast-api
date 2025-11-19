from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel, computed_feild
from typing import Annotated, Feild, Literal
import json

#helper funtion to help load data form json file
def loaddata():
    with open('patient.json' ,'r') as f:
        data = json.load(f)


    return data

app = FastAPI()

class Patient(BaseModel):
    patient_id :Annotated[ str , Feild (... , description ='id of the patient', example='P001')]
    name : Annotated[str , Feild (..., description='name pf the patietnt', example ='John Doe')]
    city : Annotated[str , Feild (..., description = 'city of the patietnt', example ='new york')]
    age : Annotated[int , Feild (..., gt=0,lt = 120,description='age of the patient', example =40)]
    gender : Annotated[Literal ['male','female','others'], Feild (..., description='gender on the patient')]
    height : Annotated[float , Feild (..., gt =0 , description = 'height of the patient in cm ', example = 175.5)]
    weight : Annotated[float , Feild (..., gt=0 ,description='weight of the patient in mtrs ',example = '70.2')] 

    @computed_feild 
    @property
    def bmi(self) -> float:
        hight_mtr = (round(self.weight/ self.height 2**),2)
        return bmi
    
    @computed_feild
    @property 
    def verdict(self) -> str :
        if self.bmi < 18.5:
            return 'underweight'
        elif 18.5 <= self.bmi < 25:
            return 'normal'
        else :
            return 'overweight'

@app.get("/")
def hello():
    return {'message' : 'Patient management system API'}

@app.get("/about")
def about():
    return {'message' : 'fully functional api to manage patient records '}

# to show the whole pateient data or data

@app.get('/view')
def view():
    data= loaddata()

    return data

# to show the data of a perticualr patient
@app.get('/patient/{patient_id}')
def patient(patient_id :str=Path (...,description='ID of patient in DB',example='P003')):
    # loading data
    data = loaddata()
    if patient_id in data :
        return data[patient_id]
    raise HTTPException(status_code=404, detail= 'patient not found' )
# if the json file was a dict contaning list or nested dict
# @app.get("/patient/{patient_id}")
# def patient(patient_id: str):
#     data = loaddata()
#     for p in data["patients"]:
#         if p["PatientID"] == patient_id:
#             return p
#     return {"error": "patient not found"}
@app.get('/sort')
def sortpatient(sortby: str =Query(...,description= 'sort ont he basis of height ,weight or bmi'),order: str = Query('asc',description='sort in asc or dec order')):

    valid_feilds = ['height','weight','bmi','age']
    if sortby not in valid_feilds:
        raise HTTPException(status_code=400,detail='invalid order slect between asc or dec')
    data = loaddata()

    sortorder= True if order == 'desc' else False
    sorted_data = sorted(data.values(),key=lambda x:x.get (sortby,0), reverse = sortorder)

    return sorted_data  

@app.post('/create')
def create_patient (patient : Patient ):
    #load existing data
    data= loaddata()

    # chick if old patient
    if patient.patient_id in data:
        raise HTTPException(status_code = 400, detail='patient already exists')

    
