from fastapi import FastAPI,Path,HTTPException,Query
import json

#helper funtion to help load data form json file
def loaddata():
    with open('patient.json' ,'r') as f:
        data = json.load(f)


    return data

app = FastAPI()

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