from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Answer, Question, Quiz, QuizTaker, UsersAnswer


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(**data)
		if user:
			return user
		raise serializers.ValidationError('Incorrect Credentials')


class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User.objects.create_user(
			first_name=validated_data["first_name"],
      last_name=validated_data["last_name"],
			username=validated_data["username"],
			email=validated_data["email"],
			password=validated_data["password"]
		)
		return user


class UserSerializer(serializers.ModelSerializer):  
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email', 'username',)

class MyQuizListSerializer(serializers.ModelSerializer):
  completed = serializers.SerializerMethodField()
  progress = serializers.SerializerMethodField()
  questions_count = serializers.SerializerMethodField()
  score = serializers.SerializerMethodField()

  class Meta:
    model = Quiz
    fields = ["id", "name", "description", "slug", "questions_count", "completed", "score", "progress", "image"]
    read_only_fields = ["questions_count", "completed", "progress"]

  def get_completed(self, obj):
    try:
      quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
      return quiztaker.completed
    except QuizTaker.DoesNotExist:
      return None

  def get_progress(self, obj):
    try:
      quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
      if quiztaker.completed == False:
        questions_answered = UsersAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count()
        total_questions = obj.question_set.all().count()
        return int(questions_answered / total_questions)
      return None
    except QuizTaker.DoesNotExist:
      return None

  def get_questions_count(self, obj):
    return obj.question_set.all().count()

  def get_score(self, obj):
    try:
      quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
      if quiztaker.completed == True:
        return quiztaker.score
      return None
    except QuizTaker.DoesNotExist:
      return None

class QuizListSerializer(serializers.ModelSerializer):
  questions_count = serializers.SerializerMethodField()
  class Meta:
    model = Quiz
    fields = ["id", "name", "description", "slug", "questions_count", "image"]
    read_only_fields = ["questions_count"]

  def get_questions_count(self, obj):
    return obj.question_set.all().count()

class AnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Answer
    fields = ["id", "question", "text"]

class QuestionSerializer(serializers.ModelSerializer):
  answer_set = AnswerSerializer(many=True)

  class Meta:
    model = Question
    fields = "__all__"

class UsersAnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = UsersAnswer
    fields = "__all__"

class QuizTakerSerializer(serializers.ModelSerializer):
  usersanswer_set = UsersAnswerSerializer(many=True)

  class Meta:
    model = QuizTaker
    fields = "__all__"

class QuizDetailSerializer(serializers.ModelSerializer):
  quiztakers_set = serializers.SerializerMethodField()
  question_set = QuestionSerializer(many=True)

  class Meta:
    model = Quiz
    fields = "__all__"

  def get_quiztakers_set(self, obj):
    try:
      quiz_taker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
      serializer = QuizTakerSerializer(quiz_taker)
      return serializer.data
    except QuizTaker.DoesNotExist:
      return None

class QuizResultSerializer(serializers.ModelSerializer):
  quiztaker_set = serializers.SerializerMethodField()
  question_set = QuestionSerializer(many=True)

  class Meta:
    model = Quiz
    fields = "__all__"

  def get_quiztaker_set(self, obj):
    try:
      quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
      serializer = QuizTakerSerializer(quiztaker)
      return serializer.data
    except QuizTaker.DoesNotExist:
      return None 