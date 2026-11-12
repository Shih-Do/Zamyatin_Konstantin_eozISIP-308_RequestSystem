from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.session import Base

class User(Base):
    __tablename__ = "Users"
<<<<<<< HEAD

=======
>>>>>>> feature/lab6
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
<<<<<<< HEAD
    
    # Связи
=======
>>>>>>> feature/lab6
    requests_authored = relationship("Request", foreign_keys="Request.author_id", back_populates="author")
    requests_assigned = relationship("Request", foreign_keys="Request.assignee_id", back_populates="assignee")

class Status(Base):
    __tablename__ = "Statuses"
<<<<<<< HEAD

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
=======
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
>>>>>>> feature/lab6
    requests = relationship("Request", back_populates="status")

class Category(Base):
    __tablename__ = "Categories"
<<<<<<< HEAD

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("Categories.id"), nullable=True)
    
=======
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("Categories.id"), nullable=True)
>>>>>>> feature/lab6
    requests = relationship("Request", back_populates="category")

class Request(Base):
    __tablename__ = "Requests"
<<<<<<< HEAD

=======
>>>>>>> feature/lab6
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, nullable=False, default="Средний")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = Column(DateTime, nullable=True)
<<<<<<< HEAD
    
=======
>>>>>>> feature/lab6
    author_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("Users.id"), nullable=True)
    status_id = Column(Integer, ForeignKey("Statuses.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("Categories.id"), nullable=False)
<<<<<<< HEAD

    # Связи (позволяют обращаться к связанным объектам, например, request.author.name)
=======
>>>>>>> feature/lab6
    author = relationship("User", foreign_keys=[author_id], back_populates="requests_authored")
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="requests_assigned")
    status = relationship("Status", back_populates="requests")
    category = relationship("Category", back_populates="requests")