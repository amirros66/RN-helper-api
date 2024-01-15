from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    tasks = relationship("Task", back_populates="patient")
    #Above relationship - mapper error was thrown when 'back_populates="patient" was plural



class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    title = Column(String)
    completed = Column(Boolean, nullable=False, default=False)
    patient = relationship("Patient", back_populates="tasks")

