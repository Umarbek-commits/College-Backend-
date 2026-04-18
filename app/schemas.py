from pydantic import BaseModel
from typing import Optional, List

# -------- TEACHER --------
class TeacherCreate(BaseModel):
    name: str


class TeacherOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------- STUDENT --------
class StudentCreate(BaseModel):
    name: str
    email: Optional[str] = None


class StudentOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

    class Config:
        from_attributes = True


# -------- COURSE --------
class CourseCreate(BaseModel):
    title: str
    teacher_id: int


class CourseOut(BaseModel):
    id: int
    title: str
    teacher_id: int

    class Config:
        from_attributes = True


# -------- NESTED --------
class CourseSimple(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class StudentWithCourses(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    courses: List[CourseSimple] = []

    class Config:
        from_attributes = True


# -------- PROFILE --------
class ProfileCreate(BaseModel):
    student_id: int
    bio: str
    age: str


class ProfileOut(BaseModel):
    id: int
    bio: str
    age: str
    student_id: int

    class Config:
        from_attributes = True


# -------- DEPARTMENT --------
class DepartmentCreate(BaseModel):
    name: str


class DepartmentOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True