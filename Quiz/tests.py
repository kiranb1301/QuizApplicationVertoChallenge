from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Quiz, Question, Option


class QuizAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.quiz = Quiz.objects.create(title="Python Basics", instructions="Answer carefully")

    def test_create_quiz(self):
        payload = {"title": "Django Basics", "instructions": "Answer all"}
        res = self.client.post("/api/quizzes/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Django Basics")

    def test_list_quizzes(self):
        res = self.client.get("/api/quizzes/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)


class QuestionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.quiz = Quiz.objects.create(title="Math Quiz")
        self.quiz_id = str(self.quiz.id)

    def test_add_question_to_quiz(self):
        payload = {
            "text": "What is 2+2?",
            "type": "single",
            "options": [
                {"text": "3", "is_correct": False},
                {"text": "4", "is_correct": True}
            ]
        }
        res = self.client.post(f"/api/quizzes/{self.quiz_id}/questions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["text"], "What is 2+2?")

    def test_list_quiz_questions(self):
        q = Question.objects.create(quiz=self.quiz, text="2+2?", type="single")
        Option.objects.create(question=q, text="4", is_correct=True)
        Option.objects.create(question=q, text="5", is_correct=False)

        res = self.client.get(f"/api/quizzes/{self.quiz_id}/all-questions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["text"], "2+2?")



class SubmissionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.quiz = Quiz.objects.create(title="Science Quiz")
        self.q1 = Question.objects.create(quiz=self.quiz, text="H2O is?", type="single")
        self.opt1 = Option.objects.create(question=self.q1, text="Water", is_correct=True)
        self.opt2 = Option.objects.create(question=self.q1, text="Oxygen", is_correct=False)

    def test_submit_answers(self):
        payload = {
            "answers": [
                {"question": str(self.q1.id), "selected_options": [str(self.opt1.id)]}
            ]
        }
        res = self.client.post(f"/api/quizzes/{self.quiz.id}/submit/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["score"], 1)
        self.assertEqual(res.data["total"], 1)


class QuizAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.quiz = Quiz.objects.create(title="Python Basics", instructions="Answer carefully")

    def test_create_quiz(self):
        payload = {"title": "Django Basics", "instructions": "Answer all"}
        res = self.client.post("/api/quizzes/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "Django Basics")

    def test_list_quizzes(self):
        res = self.client.get("/api/quizzes/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)


class QuestionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.quiz = Quiz.objects.create(title="Math Quiz")
        self.quiz_id = str(self.quiz.id)

    def test_add_question_to_quiz(self):
        payload = {
            "text": "What is 2+2?",
            "type": "single",
            "options": [
                {"text": "3", "is_correct": False},
                {"text": "4", "is_correct": True}
            ]
        }
        res = self.client.post(f"/api/quizzes/{self.quiz_id}/questions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["text"], "What is 2+2?")

    def test_list_quiz_questions(self):
        q = Question.objects.create(quiz=self.quiz, text="2+2=?", type="single")
        Option.objects.create(question=q, text="4", is_correct=True)
        Option.objects.create(question=q, text="5", is_correct=False)

        res = self.client.get(f"/api/quizzes/{self.quiz_id}/all-questions/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["text"], "2+2=?")

    # ❌ Negative: less than 2 options
    def test_invalid_question_with_one_option(self):
        payload = {
            "text": "Is Python fun?",
            "type": "single",
            "options": [
                {"text": "Yes", "is_correct": True}
            ]
        }
        res = self.client.post(f"/api/quizzes/{self.quiz_id}/questions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class SubmissionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.quiz = Quiz.objects.create(title="Science Quiz")
        self.q1 = Question.objects.create(quiz=self.quiz, text="H2O is?", type="single")
        self.opt1 = Option.objects.create(question=self.q1, text="Water", is_correct=True)
        self.opt2 = Option.objects.create(question=self.q1, text="Oxygen", is_correct=False)

    def test_submit_answers(self):
        payload = {
            "answers": [
                {"question": str(self.q1.id), "selected_options": [str(self.opt1.id)]}
            ]
        }
        res = self.client.post(f"/api/quizzes/{self.quiz.id}/submit/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["score"], 1)
        self.assertEqual(res.data["total"], 1)

    # ❌ Negative: no answers submitted
    def test_submit_no_answers(self):
        payload = {"answers": []}
        res = self.client.post(f"/api/quizzes/{self.quiz.id}/submit/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["score"], 0)
        self.assertEqual(res.data["total"], 1)

    # ❌ Negative: invalid option ID
    def test_submit_invalid_option(self):
        payload = {
            "answers": [
                {"question": str(self.q1.id), "selected_options": ["not-a-valid-id"]}
            ]
        }
        res = self.client.post(f"/api/quizzes/{self.quiz.id}/submit/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)  # still processes
        self.assertEqual(res.data["score"], 0)

    # ❌ Negative: text answer too long
    def test_submit_text_answer_too_long(self):
        q2 = Question.objects.create(quiz=self.quiz, text="Explain gravity", type="text")
        long_text = "a" * 400  # 400 chars
        payload = {
            "answers": [
                {"question": str(q2.id), "text_answer": long_text}
            ]
        }
        res = self.client.post(f"/api/quizzes/{self.quiz.id}/submit/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(res.data["answers"][0]["text_answer"]), 300)
