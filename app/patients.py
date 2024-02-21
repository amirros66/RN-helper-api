from sqlalchemy.orm import Session
from . import models, schemas


#get patients
def get_patients(db: Session, skip: int = 0, limit: int = 20):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    print(patients)
    return patients

#create patient
def create_patient(db: Session, patient: schemas.Patient):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

#delete patient
def delete_patient(db: Session, patient_id: int):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    db.delete(patient)
    db.commit()
    return patient

#get one patient
def get_patient(db: Session, patient_id: int):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    print(patient)
    return patient

#get patient by name
def get_patient_by_name(db: Session, name: str):
    patient = db.query(models.Patient).filter(models.Patient.name == name).first()
    print(patient)
    return patient

########Delete all patients
def delete_all_patients(db: Session):
    db.query(models.Patient).delete()
    db.commit()