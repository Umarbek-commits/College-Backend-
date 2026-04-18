from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import models
from app.schemas import (
    StudentCreate, StudentOut, StudentWithCourses,
    TeacherCreate, TeacherOut,
    CourseCreate, CourseOut,
    ProfileCreate, ProfileOut,
    DepartmentCreate, DepartmentOut
)

# ✅ ПРАВИЛЬНОЕ СОЗДАНИЕ FASTAPI
app = FastAPI(
    title="🎓 College API",
    description="API для управления студентами, курсами и преподавателями",
    version="1.0.0"
)

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
    return {"message": "API works"}


# ---------------- TEACHER ----------------
@app.post(
    "/teachers/",
    response_model=TeacherOut,
    tags=["Teachers"],
    summary="Создать преподавателя",
    description="Создает нового преподавателя с указанием имени"
)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(name=teacher.name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@app.get(
    "/teachers/",
    response_model=list[TeacherOut],
    tags=["Teachers"],
    summary="Получить всех преподавателей",
    description="Возвращает список всех преподавателей"
)
def get_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()


# ---------------- STUDENT ----------------
@app.post(
    "/students/",
    response_model=StudentOut,  # ✅ ИСПРАВЛЕНО: StudentResponse → StudentOut
    tags=["Students"],
    summary="Создать студента",
    description="Создает нового студента с именем и email"
)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Проверяем, не существует ли студент с таким email
    if student.email:
        existing_student = db.query(models.Student).filter(
            models.Student.email == student.email
        ).first()
        
        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="Student with this email already exists"
            )
    
    db_student = models.Student(
        name=student.name,
        email=student.email
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get(
    "/students/",
    response_model=list[StudentWithCourses],
    tags=["Students"],
    summary="Получить всех студентов",
    description="Возвращает список всех студентов с их курсами и профилями"
)
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.get(
    "/students/{student_id}",
    response_model=StudentWithCourses,
    tags=["Students"],
    summary="Получить студента по ID",
    description="Возвращает информацию о конкретном студенте"
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    
    return student


@app.get(
    "/students/search/",
    response_model=list[StudentOut],  # ✅ ИСПРАВЛЕНО: StudentResponse → StudentOut
    tags=["Students"],
    summary="Поиск студента по имени",
    description="Ищет студентов по точному совпадению имени"
)
def search_student(name: str, db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.name == name).all()
    
    if not students:
        raise HTTPException(
            status_code=404,
            detail=f"No students found with name '{name}'"
        )
    
    return students


@app.delete(
    "/students/{student_id}",
    tags=["Students"],
    summary="Удалить студента",
    description="Удаляет студента из базы данных"
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    
    db.delete(student)
    db.commit()
    
    return {"message": f"Student '{student.name}' deleted successfully"}


@app.put(
    "/students/{student_id}",
    response_model=StudentOut,  # ✅ ИСПРАВЛЕНО: StudentResponse → StudentOut
    tags=["Students"],
    summary="Обновить студента",
    description="Обновляет имя и email студента"
)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    
    if not db_student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    
    # Проверяем email на уникальность (если меняется)
    if student.email and db_student.email != student.email:
        existing = db.query(models.Student).filter(
            models.Student.email == student.email
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Student with this email already exists"
            )
    
    db_student.name = student.name
    db_student.email = student.email
    db.commit()
    db.refresh(db_student)
    
    return db_student


# ---------------- COURSE ----------------
@app.post(
    "/courses/",
    response_model=CourseOut,
    tags=["Courses"],
    summary="Создать курс",
    description="Создает новый курс с указанием названия и ID преподавателя"
)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли преподаватель
    teacher = db.query(models.Teacher).filter(
        models.Teacher.id == course.teacher_id
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=404,
            detail=f"Teacher with id {course.teacher_id} not found"
        )
    
    db_course = models.Course(
        title=course.title,
        teacher_id=course.teacher_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get(
    "/courses/",
    response_model=list[CourseOut],
    tags=["Courses"],
    summary="Получить все курсы",
    description="Возвращает список всех курсов"
)
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


# ---------------- ENROLL ----------------
@app.post(
    "/enroll/",
    tags=["Enrollment"],
    summary="Записать студента на курс",
    description="Добавляет студента на указанный курс"
)
def enroll_student(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    course = db.query(models.Course).filter(models.Course.id == course_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )

    if not course:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id {course_id} not found"
        )
    
    # Проверяем, не записан ли уже студент
    if course in student.courses:
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled in this course"
        )

    student.courses.append(course)
    db.commit()

    return {"message": f"Student '{student.name}' enrolled in course '{course.title}'"}


# ---------------- PROFILE ----------------
@app.post(
    "/profiles/",
    response_model=ProfileOut,
    tags=["Profiles"],
    summary="Создать профиль студента",
    description="Создает профиль для студента с биографией и возрастом"
)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли студент
    student = db.query(models.Student).filter(
        models.Student.id == profile.student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {profile.student_id} not found"
        )
    
    # Проверяем, нет ли уже профиля
    existing_profile = db.query(models.Profile).filter(
        models.Profile.student_id == profile.student_id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists for this student"
        )
    
    db_profile = models.Profile(
        student_id=profile.student_id,
        bio=profile.bio,
        age=profile.age
    )
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    return db_profile


@app.get(
    "/profiles/",
    response_model=list[ProfileOut],
    tags=["Profiles"],
    summary="Получить все профили",
    description="Возвращает список всех профилей студентов"
)
def get_profiles(db: Session = Depends(get_db)):
    return db.query(models.Profile).all()


@app.get(
    "/profiles/{student_id}",
    response_model=ProfileOut,
    tags=["Profiles"],
    summary="Получить профиль по ID студента",
    description="Возвращает профиль конкретного студента"
)
def get_profile_by_student(student_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(
        models.Profile.student_id == student_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Profile for student {student_id} not found"
        )
    
    return profile


# ---------------- DEPARTMENT ----------------
@app.post(
    "/departments/",
    response_model=DepartmentOut,
    tags=["Departments"],
    summary="Создать департамент",
    description="Создает новый департамент"
)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = models.Department(name=department.name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@app.get(
    "/departments/",
    response_model=list[DepartmentOut],
    tags=["Departments"],
    summary="Получить все департаменты",
    description="Возвращает список всех департаментов"
)
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


@app.get(
    "/departments/{department_id}",
    response_model=DepartmentOut,
    tags=["Departments"],
    summary="Получить департамент по ID",
    description="Возвращает информацию о конкретном департаменте"
)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(
        models.Department.id == department_id
    ).first()
    
    if not department:
        raise HTTPException(
            status_code=404,
            detail=f"Department with id {department_id} not found"
        )
    
    return department