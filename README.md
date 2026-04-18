# 🎓 College Management API

## 📌 Описание
Backend API для управления колледжем.  
Позволяет работать со студентами, преподавателями, курсами и их связями.

---

## 🧱 Технологии

- ⚡ FastAPI
- 🧠 SQLAlchemy (ORM)
- 🗄 SQLite
- 📦 Pydantic

---

## 📂 Основные сущности

- 👨‍🎓 **Student** — студент
- 👨‍🏫 **Teacher** — преподаватель
- 📚 **Course** — курс
- 📄 **Profile** — профиль студента
- 🏢 **Department** — департамент

---

## 🔗 Связи

- 🔹 Teacher → Course (**One-to-Many**)  
- 🔹 Student ↔ Course (**Many-to-Many**)  
- 🔹 Student → Profile (**One-to-One**)

---

## 🚀 Возможности

- ✅ CRUD для студентов, курсов и преподавателей  
- ✅ Запись студента на курс  
- ✅ Получение связанных данных (курсы студента)  
- ✅ Поиск студентов  
- ✅ Валидация данных (Pydantic)  
- ✅ Обработка ошибок (HTTPException)  
- ✅ REST API с документацией  

---

## 📖 API Документация

После запуска доступно:

- Swagger UI:  
  👉 http://127.0.0.1:8000/docs  

- ReDoc:  
  👉 http://127.0.0.1:8000/redoc  

---

## ▶️ Запуск проекта

### 1. Установить зависимости

```bash
pip install -r requirements.txt