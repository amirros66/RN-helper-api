from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import patients, models, database, schemas, tasks

# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Endpoints to work with patients


#Patients
#Get Patient (with its items)
@app.get("/patients", response_model=List[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = patients.get_patients(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No patients found")
    return results

#Create Patient
@app.post("/patients", response_model=schemas.PatientBase)
def create_patient(patient: schemas.PatientBase, db: Session = Depends(get_db)):
    return patients.create_patient(db, patient=patient)

#Delete Patient
@app.delete("/patient", response_model=schemas.Patient)
def delete_patients(patient_id: int, db: Session = Depends(get_db)):
    return patients.delete_patient(db, patient_id=patient_id)

#########Delete all patients
@app.delete("/patients")
def delete_all_patients_endpoint(db: Session = Depends(get_db)):
    patients.delete_all_patients(db)
    return {"message": "All patients have been deleted"}


#Tasks
#Get tasks from a patient
@app.get("/patient/{patient_id}/tasks", response_model=List[schemas.Task])
def read_patient_tasks(patient_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = tasks.get_tasks(db, patient_id=patient_id, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No tasks found")
    return results

#Create task
@app.post("/patient/{patient_id}/tasks", response_model=schemas.Task)
def create_patient_task(patient_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return tasks.create_task(db, patient_id=patient_id, task=task)


#Delete one task by patient id
@app.delete("/patient/{patient_id}/tasks", response_model=schemas.Task)
def delete_patient_task(patient_id: int, task_id: int, db: Session = Depends(get_db)):
    return tasks.delete_task(db, patient_id=patient_id, task_id=task_id)

#Delete all tasks by patient id
@app.delete("/patient/{patient_id}/tasks/all")
def delete_all_patient_tasks(patient_id: int, db: Session = Depends(get_db)):
    tasks.delete_patient_tasks(db, patient_id=patient_id)
    return {"message": f"All tasks for patient {patient_id} have been deleted"}


#Delete all tasks
@app.delete("/patients/tasks")
def delete_all_tasks_endpoint(db: Session = Depends(get_db)):
    tasks.delete_all_tasks(db)
    return {"message": "All tasks have been deleted"}


@app.patch("/tasks/{task_id}/toggle")
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    updated_task = tasks.toggle_task_completion(db, task_id=task_id)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task