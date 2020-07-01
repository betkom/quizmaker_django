from django.contrib import admin

import nested_admin

from .models import Quiz, Question, Answer, Response, QuizTaker, UsersAnswer

class AnswerInline(nested_admin.NestedTabularInline):
  model = Answer
  extra = 4
  max_num = 4
class QuestionInline(nested_admin.NestedTabularInline):
  model = Question
  inlines = [AnswerInline,]
  extra = 19
class QuizAdmin(nested_admin.NestedModelAdmin):
  inlines = [QuestionInline,]
class ResponseInline(admin.TabularInline):
  model = Response
class QuizTakerAdmin(admin.ModelAdmin):
  inlines = [ResponseInline,]
class UsersAnswerInline(admin.TabularInline):
  model = UsersAnswer

admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizTaker, QuizTakerAdmin)
admin.site.register(Answer)
admin.site.register(UsersAnswer)
