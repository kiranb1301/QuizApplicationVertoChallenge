from rest_framework import serializers
from .models import Quiz, Question, Submission, SubmissionAnswer, Option


class QuizSerializer(serializers.ModelSerializer):
    total_marks = serializers.ReadOnlyField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'instructions', 'created_at', 'total_marks']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'type', 'order', 'marks', 'options']

    def validate(self, attrs):
        q_type = attrs.get('type')
        options = self.initial_data.get('options', [])

        # --- Text Question Rules ---
        if q_type == Question.TEXT:
            if options:
                raise serializers.ValidationError("Text-based questions cannot have options.")
            if len(attrs.get("text", "")) > 300:
                raise serializers.ValidationError("Text-based question text cannot exceed 300 characters.")
            return attrs

        # --- Choice Question Rules ---
        if not options or len(options) < 2:
            raise serializers.ValidationError("Choice questions must have at least two options.")

        correct_count = sum(1 for o in options if o.get("is_correct"))

        if q_type == Question.SINGLE and correct_count != 1:
            raise serializers.ValidationError("Single-choice questions must have exactly one correct option.")

        if q_type == Question.MULTIPLE and correct_count < 1:
            raise serializers.ValidationError("Multiple-choice questions must have at least one correct option.")

        return attrs

    def create(self, validated_data):
        options_data = validated_data.pop("options", [])
        question = Question.objects.create(**validated_data)

        if question.type in [Question.SINGLE, Question.MULTIPLE]:
            for opt in options_data:
                Option.objects.create(
                    question=question,
                    text=opt["text"],
                    is_correct=opt.get("is_correct", False),
                )
        return question

class PublicMCQQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'type', 'order', 'options']

    def get_options(self, obj):
        # return only id & text (hide is_correct)
        return [{"id": opt.id, "text": opt.text} for opt in obj.options.all()]


class SubmissionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAnswer
        fields = ['id', 'question', 'selected_options', 'text_answer']


class SubmissionSerializer(serializers.ModelSerializer):
    #answers = SubmissionAnswerSerializer(many=True, required=False)

    class Meta:
        model = Submission
        fields = ['id', 'quiz', 'score', 'total', 'submitted_at'] #'answers']
        read_only_fields = ['score', 'total', 'submitted_at']
