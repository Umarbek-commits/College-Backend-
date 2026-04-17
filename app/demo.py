from app.database import SessionLocal
from app import models

db = SessionLocal()

# CREATE
student1 = models.Student(name="Umar")
student2 = models.Student(name="Aibek")

teacher = models.Teacher(name="Mr. Smith")

db.add_all([student1, student2, teacher])
db.commit()

course = models.Course(title="Math", teacher_id=teacher.id)
db.add(course)
db.commit()

# ENROLL
student1.courses.append(course)
db.commit()

# PROFILE (1:1)
profile = models.Profile(student_id=student1.id, bio="Top student", age=18)
db.add(profile)
db.commit()

# READ
print("Students:", db.query(models.Student).all())

# UPDATE
student1.name = "Umar Updated"
db.commit()

# DELETE (пример)
# db.delete(student2)
# db.commit()

db.close()