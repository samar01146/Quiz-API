from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD_COURSE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class AddCourse(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return str(self.course_name)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD_QUESTION AND OPTION<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class AddQuestion(models.Model):
    course = models.ForeignKey(
        AddCourse, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=100)
    option = models.CharField(max_length=120)

    def __str__(self):
        return str(self.question)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD_STUDENT_ANSWER<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class YourAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(AddQuestion, on_delete=models.CASCADE)
    your_answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.question)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ADD_RIGHT_ANSWER<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class ShowQuestion(models.Model):
    course = models.ForeignKey(AddCourse, on_delete=models.CASCADE)
    question = models.ForeignKey(AddQuestion, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.course)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SUBMIT_EXAM<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class SubmitExam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_marks = models.CharField(max_length=100)
    percentage = models.CharField(max_length=50)

    def __str__(self):
        return str(self.user)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>STUDENT_COURSE_NAME<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


class StudentCourse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.OneToOneField(
        AddCourse, on_delete=models.CASCADE, null=True)
    stu_course = models.CharField(max_length=100)

    def __str__(self):
        return str(self.stu_course)
