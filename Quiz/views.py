from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Quiz, Question, Option, Submission, SubmissionAnswer
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    PublicMCQQuestionSerializer,
    SubmissionSerializer,
)
from uuid import UUID
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# ---------------- QUIZZES ----------------
class QuizListCreateAPIView(APIView):
    """Create new quiz or list all quizzes."""

    def get(self, request):
        try:
            quizzes = Quiz.objects.all().order_by('-created_at')
            serializer = QuizSerializer(quizzes, many=True)

            # Only return subset of fields
            slim_data = [
                {"id": q["id"], "title": q["title"]}
                for q in serializer.data
            ]
            return Response(slim_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=QuizSerializer,   # ✅ tells Swagger what to expect
        responses={201: QuizSerializer}
    )
    def post(self, request):
        try:
            serializer = QuizSerializer(data=request.data)
            if serializer.is_valid():
                quiz = serializer.save()
                return Response(
                    QuizSerializer(quiz).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateQuestions(APIView):
    """Create and List Questions for a Particular Quiz"""

    def post(self, request, quiz_id):
        try:
            quiz = get_object_or_404(Quiz, id=quiz_id)

            # Inject quiz into payload
            data = request.data.copy()
            data['quiz'] = str(quiz.id)

            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():
                question = serializer.save()
                return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, quiz_id):
        """List all questions for this quiz (hide correct answers)."""
        try:
            quiz = get_object_or_404(Quiz, id=quiz_id)
            questions = quiz.questions.prefetch_related("options").all()
            serializer = PublicMCQQuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuizDetailAPIView(APIView):
    """Retrieve, update, or delete a quiz."""

    def get(self, request, pk):
        try:
            quiz = get_object_or_404(Quiz, pk=pk)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            quiz = get_object_or_404(Quiz, pk=pk)
            serializer = QuizSerializer(quiz, data=request.data, partial=True)
            if serializer.is_valid():
                quiz = serializer.save()
                return Response(QuizSerializer(quiz).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            quiz = get_object_or_404(Quiz, pk=pk)
            quiz.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class QuizQuestionsAPIView(APIView):
    """Get all questions for a quiz (hide correct answers)."""

    def get(self, request, quiz_id):
        try:
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            questions = quiz.questions.prefetch_related('options').all()
            serializer = PublicMCQQuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuizSubmitAPIView(APIView):
    """Submit answers and calculate score."""

    def post(self, request, quiz_id):
        try:
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            answers_payload = request.data.get('answers', [])

            total = quiz.total_marks
            score = 0

            submission = Submission.objects.create(quiz=quiz, total=total, score=0)

            for ans in answers_payload:
                qid = ans.get('question')
                selected_ids = ans.get('selected_options', [])
                text_answer = ans.get('text_answer', '')

                question = get_object_or_404(Question, id=qid, quiz=quiz)
                sub_ans = SubmissionAnswer.objects.create(submission=submission, question=question)

                if question.type in [Question.SINGLE, Question.MULTIPLE]:
                    # ✅ filter out invalid UUIDs
                    valid_ids = []
                    for sid in selected_ids:
                        try:
                            valid_ids.append(UUID(sid))
                        except Exception:
                            continue  
                    options = Option.objects.filter(id__in=valid_ids, question=question)
                    sub_ans.selected_options.set(options)

                    correct_ids = set(question.options.filter(is_correct=True).values_list('id', flat=True))
                    chosen_ids = set(options.values_list('id', flat=True))
                    if correct_ids == chosen_ids:
                        score += question.marks

                else:  # text question
                    sub_ans.text_answer = text_answer[:300]
                    sub_ans.save()

            submission.score = score
            submission.save(update_fields=['score'])

            # Use serializer for consistent response
            serializer = SubmissionSerializer(submission)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuestionDetailAPIView(APIView):
    """Retrieve, update, or delete a question."""

    def get(self, request, pk):
        try:
            question = get_object_or_404(Question, pk=pk)
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            question = get_object_or_404(Question, pk=pk)
            serializer = QuestionSerializer(question, data=request.data, partial=True)
            if serializer.is_valid():
                question = serializer.save()
                return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            question = get_object_or_404(Question, pk=pk)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
