from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import models
from app import schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)

# dependency (подключение к БД)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "College API works"}


# ---------------- TEACHER ----------------
@app.post("/teachers/", response_model=schemas.TeacherOut)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(name=teacher.name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@app.get("/teachers/")
def get_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()


# ---------------- STUDENT ----------------
@app.post("/students/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=list[schemas.StudentWithCourses])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    
    return {"message": "Student deleted"}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_student.name = student.name
    db.commit()
    db.refresh(db_student)
    
    return {"message": "Student updated", "student": db_student}


# ---------------- COURSE ----------------
@app.post("/courses/", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(
        title=course.title,
        teacher_id=course.teacher_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/courses/")
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

# ---------------- ENROLL (ОБНОВЛЕННЫЙ) ----------------
@app.post("/enroll/")
def enroll_student(student_id: int, course_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    course = db.query(models.Course).filter(models.Course.id == course_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    student.courses.append(course)
    db.commit()

    return {"message": "Student enrolled in course"}