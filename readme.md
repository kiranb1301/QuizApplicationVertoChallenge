# 🎯 Online Quiz Application API

A backend API for creating and managing quizzes, adding questions, and submitting answers with scoring.  
Built using **Python + Django REST Framework** for the Verto hiring challenge.

---

## 🚀 Features

- **Quiz Management**
  - Create, list, update, and delete quizzes
  - Add questions with multiple options (single choice, multiple choice, text)
  - Validation: text questions ≤ 300 chars, choice questions must have correct answers

- **Quiz Taking**
  - Fetch quiz questions (correct answers hidden)
  - Submit answers → get back `{ "score": 3, "total": 5 }`

- **Submissions**
  - Stores quiz attempts with per-question answers
  - Supports text and MCQ-based evaluation
  - Prevents invalid inputs (wrong option IDs, long text answers)

- **API Documentation**
  - Swagger UI → `/swagger/`
  - ReDoc → `/redoc/`

- **Unit Tests**
  - Covers quiz CRUD, question validation, submission scoring, and edge cases

---

## 🛠️ Tech Stack

- Python 3.11
- Django 4.x
- Django REST Framework
- drf-yasg (Swagger/Redoc API docs)
- SQLite (default, can switch to Postgres/MySQL)

---

## 📦 Setup & Installation

```bash
# Clone repository
git clone https://github.com/<your-username>/QuizApplicationVertoChallenge.git
cd QuizApplicationVertoChallenge

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
