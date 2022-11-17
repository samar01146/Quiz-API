from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(AddCourse)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','course_name', 'description']

@admin.register(AddQuestion)
class AddquestionAdmin(admin.ModelAdmin):
    list_display = ['id','question', 'course' , 'option']

@admin.register(YourAnswer)
class answerAdmin(admin.ModelAdmin):
    list_display = ['id','user','question' , 'your_answer']

@admin.register(ShowQuestion)
class ShowQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'course','question',   'right_answer']

@admin.register(SubmitExam)
class SubmitExamAdmin(admin.ModelAdmin):
    list_display = [ 'user','total_marks',]


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'stu_course']