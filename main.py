from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse 
from pydantic import BaseModel,Field, computed_field
from typing import Annotated, Literal
import json 


app = FastAPI()

class Patient(BaseModel):
    #creating feilds for patient model
    patient_id :Annotated[ str , Field (... , description ='id of the patient', example='P001')]
    #patienit id is unique key  hence the feild name used as key in json file
    name : Annotated[str , Field (..., description='name pf the patietnt', example ='John Doe')]
    city : Annotated[str , Field (..., description = 'city of the patietnt', example ='new york')]
    age : Annotated[int , Field (..., gt=0,lt = 120,description='age of the patient', example =40)]
    gender : Annotated[Literal ['male','female','others'],Field (..., description='gender on the patient')]
    height : Annotated[float , Field (..., gt =0 , description = 'height of the patient in cm ', example = 1.5)]
    weight : Annotated[float , Field (..., gt=0 ,description='weight of the patient in mtrs ',example = '70.2')] 

    @computed_field 
    @property
    def bmi(self) -> float:

        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property 
    def verdict(self) -> str :
        if self.bmi < 18.5:
            return 'underweight'
        elif 18.5 <= self.bmi < 25:
            return 'normal'
        else :
            return 'overweight'


#helper funtion to help load data form json file
def loaddata():
    with open('patient.json' ,'r') as f:
        data = json.load(f)
    return data

#to save datat strored in post request to jason file
def savedata(data):
    with open ('patient.json','w') as f:
        json.dump(data,f)


    
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
    # add new patient 
    data[patient.patient_id] = patient.model_dump(exclude=["patient_id"])
       #cretaes a new key in data key = pateintid 
      # patient.modeldump converts pydantic object into dictionary
   #exclude must only contain feild name not dot notation 
    

    #save the data into the json file 
    savedata(data)

    return JSONResponse(status_code=201, content={'message':'patientint created sucessfully'})
    
