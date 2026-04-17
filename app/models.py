from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

# MANY-TO-MANY (Student <-> Course)
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id"))
)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    # One-to-Many (Teacher -> Courses)
    courses = relationship("Course", back_populates="teacher")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    # связь с teacher
    teacher = relationship("Teacher", back_populates="courses")

    # Many-to-Many со студентами
    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    # Many-to-Many с курсами
    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )
    
    # One-to-One с профилем
    profile = relationship("Profile", back_populates="student", uselist=False)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String)
    age = Column(Integer)

    student_id = Column(Integer, ForeignKey("students.id"), unique=True)

    student = relationship("Student", back_populates="profile")