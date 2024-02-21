from sqlalchemy.orm import Session
from . import models, schemas


#get tasks
def get_tasks(db: Session, patient_id: int, skip: int = 0, limit: int = 20):
    tasks = db.query(models.Task).filter_by(patient_id=patient_id).offset(skip).limit(limit).all() 
    print(tasks)
    return tasks

#create tasks on a patient
def create_task(db: Session, patient_id: int, task: schemas.Task):
    db_task = models.Task(**task.dict(), patient_id=patient_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

#delete task
def delete_task(db: Session, patient_id: int, task_id: int):
    task = db.query(models.Task).filter(models.Patient.id == patient_id, models.Task.id == task_id).first()
    db.delete(task)
    db.commit()
    return task

#get one task by id
def get_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    print(task)
    return task

#get task by title
def get_task_by_title(db: Session, title: str):
    task = db.query(models.Task).filter(models.Task.title == title).first()
    print(task)
    return task

#Delete tasks by patient id
def delete_patient_tasks(db: Session, patient_id: int):
    tasks_to_delete = db.query(models.Task).filter(models.Task.patient_id == patient_id)
    tasks_to_delete.delete(synchronize_session=False)
    db.commit()


#delete_all_tasks
def delete_all_tasks(db: Session):
    db.query(models.Task).delete()
    db.commit()