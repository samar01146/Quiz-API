from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import *


class StudentRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password',  'confirm_password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField()


class AddQuestionSerializer(serializers.ModelSerializer):
    # course = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = AddQuestion
        fields = ['id', 'question', 'option']

    def to_representation(self, instance):
        a = instance.option.split(",")
        data = {
            "id": instance.id,
            "question": instance.question,
            "answer": {
                "OPTIONS1": a[0],
                "OPTIONS2": a[1],
                "OPTIONS3": a[2],
                "OPTIONS4": a[3],
            }
        }
        return data


class CourseSerializer(serializers.ModelSerializer):
    questions = AddQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AddCourse
        fields = ['course_name', 'description', 'questions']


class AnswerSerialization(serializers.ModelSerializer):
    # question= serializers.StringRelatedField(read_only=True)
    class Meta:
        model = YourAnswer
        fields = ['question', 'your_answer']


class ShowQuestionSerialization(serializers.ModelSerializer):
    question = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ShowQuestion
        fields = ['id', 'course', 'question']


class SubmitExamSerialization(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SubmitExam
        fields = ['user', 'total_marks']


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddCourse
        fields = ['id', 'course_name']
