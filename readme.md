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
- Django 5.x
- Django REST Framework
- drf-yasg (Swagger/Redoc API docs)
- SQLite (default, can switch to Postgres/MySQL)

---

## 📦 Setup & Installation

```bash
# Clone repository
git clone https://github.com/kiranb1301/QuizApplicationVertoChallenge.git
cd QuizApplicationVertoChallenge

# Create virtual environment
python -m venv myenv
source myenv/bin/activate   # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## 🔗 Repository

- GitHub: [kiranb1301/QuizApplicationVertoChallenge](https://github.com/kiranb1301/QuizApplicationVertoChallenge)

---

## ▶️ Running Locally

- App base URL (after starting): `http://127.0.0.1:8000/`
- API base path: `http://127.0.0.1:8000/api/`
- API docs: `http://127.0.0.1:8000/swagger/` and `http://127.0.0.1:8000/redoc/`

---

## ✅ Running Tests

```bash
python manage.py test
```

This runs the Django test suite using an ephemeral SQLite test database.

---

## 🔌 Quick Endpoint Reference

- POST `/api/quizzes/` — create quiz
- GET `/api/quizzes/` — list quizzes (returns only `id` and `title`)
- GET `/api/quizzes/{quiz_id}/` — get quiz detail
- PUT `/api/quizzes/{quiz_id}/` — update quiz
- DELETE `/api/quizzes/{quiz_id}/` — delete quiz
- POST `/api/quizzes/{quiz_id}/questions/` — add question to quiz
- GET `/api/quizzes/{quiz_id}/all-questions/` — list questions (options hide `is_correct`)
- POST `/api/quizzes/{quiz_id}/submit/` — submit answers and get score
- GET/PUT/DELETE `/api/questions/{question_id}/` — question detail/update/delete

---

## 🧠 Assumptions & Design Choices

- IDs use UUIDv4 for quizzes, questions, options, and submissions.
- Validation rules enforced in serializers:
  - Text questions: no options allowed; text ≤ 300 characters.
  - Choice questions: at least 2 options; single-choice requires exactly 1 correct; multiple-choice requires ≥ 1 correct.
- Questions listing hides `is_correct` to prevent leaking answers.
- Scoring for choice questions requires an exact match of all correct options; partial matches score 0. Text questions are stored but not auto-scored.
- Submission API is tolerant to invalid option IDs; they are ignored safely.
- Pagination enabled globally via DRF with page size 5 (affects list endpoints).
- API-only responses default to JSON; browsable API is disabled for performance consistency.
- Local development uses SQLite; production can switch databases via `DATABASES` settings.
- API documentation provided via Swagger and Redoc using `drf-yasg`.
- Default `DEBUG=True` for local use; do not use in production.

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

