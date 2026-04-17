from pydantic import BaseModel, Field

# -------- TEACHER --------
class TeacherCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class TeacherOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------- STUDENT --------
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class StudentOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# -------- COURSE --------
class CourseCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
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
    courses: list[CourseSimple]

    class Config:
        from_attributes = True