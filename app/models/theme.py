from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class Theme(BaseModel):
    __tablename__ = "themes"

    name = Column(String(256), unique=False, nullable=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    order = Column(Integer, nullable=False, default=0)
    subject = relationship("Subject", back_populates="themes", uselist=False)
    questions = relationship("Question", back_populates="theme")

    def __repr__(self):
        return f"<Theme {self.name}>"
