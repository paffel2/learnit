from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from .base import BaseModel
from sqlalchemy.orm import relationship


class Question(BaseModel):
    __tablename__ = "questions"

    name = Column(String(256), unique=True, nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=True)
    subject = relationship("Subject", back_populates="questions", uselist=False)
    theme = relationship("Theme", back_populates="questions", uselist=False)
    text = Column(String, nullable=True)
    order = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Question {self.name}>"
