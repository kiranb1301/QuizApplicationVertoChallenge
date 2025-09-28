from django.urls import path
from .views import (
    QuizListCreateAPIView,
    QuizDetailAPIView,
    CreateQuestions,
    QuizQuestionsAPIView,
    QuizSubmitAPIView,
    QuestionDetailAPIView,
)

urlpatterns = [
    # Quiz endpoints
    path('quizzes/', QuizListCreateAPIView.as_view(), name='quiz-list-create'),
    path('quizzes/<uuid:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('quizzes/<uuid:quiz_id>/questions/', CreateQuestions.as_view(), name='quiz-questions-create'),
    path('quizzes/<uuid:quiz_id>/all-questions/', QuizQuestionsAPIView.as_view(), name='quiz-questions'),
    path('quizzes/<uuid:quiz_id>/submit/', QuizSubmitAPIView.as_view(), name='quiz-submit'),

    # Question endpoints
    path('questions/<uuid:pk>/', QuestionDetailAPIView.as_view(), name='question-detail'),
]
