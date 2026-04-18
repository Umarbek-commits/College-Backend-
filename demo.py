from app.database import SessionLocal, engine
from app import models
from app.models import Base
from app.models import Student

# 🔥 ОБЯЗАТЕЛЬНО - создаем таблицы ДО создания сессии
Base.metadata.create_all(bind=engine)

# Теперь создаем сессию
db = SessionLocal()

# CREATE
student1 = models.Student(name="Umar", email="umar@example.com")
student2 = models.Student(name="Aibek", email="aibek@example.com")

teacher = models.Teacher(name="Mr. Smith")

db.add_all([student1, student2, teacher])
db.commit()

# Создаем курс (нужен teacher.id после коммита)
course = models.Course(title="Math", teacher_id=teacher.id)
db.add(course)
db.commit()

# ENROLL (записываем студента на курс)
student1.courses.append(course)
db.commit()

# PROFILE (1:1) - age теперь String
profile = models.Profile(student_id=student1.id, bio="Top student", age="18")
db.add(profile)
db.commit()

# НОВЫЙ КРАСИВЫЙ ВЫВОД
print("\n" + "="*50)
print("СТУДЕНТЫ И ИХ КУРСЫ")
print("="*50)

students = db.query(Student).all()

for student in students:
    print(f"👤 {student.name} ({student.email})")
    
    if student.profile:
        print(f"   📄 Profile: age={student.profile.age}, bio={student.profile.bio}")
    
    for course in student.courses:
        print(f"   📚 Course: {course.title} (Teacher: {course.teacher.name})")
    
    print()

# UPDATE
student1.name = "Umar Updated"
db.commit()
print(f"✅ Updated student name: {student1.name}")

# READ with relationship
print(f"\n📖 {student1.name} is enrolled in: {[course.title for course in student1.courses]}")
print(f"👨‍🏫 Course {course.title} has teacher: {course.teacher.name}")
print(f"👤 {student1.name} has profile: age={student1.profile.age}, bio={student1.profile.bio}")

# DELETE (пример - закомментировано)
# db.delete(student2)
# db.commit()

# Закрываем сессию
db.close()