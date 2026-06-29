from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from .base import BaseModel
from sqlalchemy.orm import relationship


class Subject(BaseModel):
    __tablename__ = "subjects"

    name = Column(String(256), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="subjects", uselist=False)
    themes = relationship("Theme", back_populates="subject")
    questions = relationship("Question", back_populates="subject")
    order = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Subject {self.name}>"
