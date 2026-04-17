# College Backend API

## 📌 Описание
Backend API для управления колледжем: студенты, курсы, преподаватели

## 🧱 Технологии
- FastAPI
- SQLAlchemy (ORM)
- SQLite

## 📂 Модели
- Student
- Teacher
- Course

## 🔗 Связи
- Teacher → Course (One-to-Many)
- Student ↔ Course (Many-to-Many)

## 🚀 Возможности
- CRUD для студентов, курсов и преподавателей
- Запись студента на курс
- Валидация данных (Pydantic)
- Обработка ошибок (HTTPException)

## ▶️ Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload


