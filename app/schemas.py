from typing import Union
from pydantic import BaseModel



#Task stuff
class TaskBase(BaseModel):
    id: int
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class Task(TaskBase):
    patient_id: int

    class Config:
        orm_mode = True


#Patient List 
class PatientBase(BaseModel):
    id: int
    name: str


class PatientCreate(BaseModel):
    name: str


class Patient(PatientBase):
    tasks: list[Task] = []

    class Config:
        orm_mode = True

