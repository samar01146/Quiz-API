from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .serializers import *

# Create your views here.
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>TOKEN<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>REGISTRATION<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class UserRegistration(APIView):
    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']
        if password == confirm_password:
            serializer.save()
            return Response({"msg": "you have sucessfully done your Registration"})
        else:
            return Response({'message': "you password didn't match please try again later"})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>LOGIN<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class UserLogin(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            subject = "DRF AUTH TESTING MAIL"
            message = "this is message for OTP"
            from_email='pma1.globaliasoft@gmail.com'
            recipient_list=['sth.globaliasoft@gmail.com',]
            send_mail(subject,message,from_email,recipient_list)
            login(request, user)
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        return Response({'errors': {'non_field_errors': ['Username or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>COURSE VIEW<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class CourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            courses = AddCourse.objects.get(id=id)
            serializers = AddCourseSerializer(courses)
            return Response({'data': serializers.data})
        courses = AddCourse.objects.all()
        serializers = AddCourseSerializer(courses, many=True)
        return Response({'data': serializers.data})

    def post(self, request):
        data = request.data
        serializers = AddCourseSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        courses_name = request.data.get("course_name")
        match_course = AddCourse.objects.filter(id=courses_name).first().id
        studentCourse = StudentCourse.objects.filter(user=request.user).first()
        if studentCourse:
            return Response({"message": "you already choosed your course cannot select again "})
        StudentCourse.objects.update_or_create(
            user=request.user, stu_course=match_course)
        return Response({"message": "okay you can start your exam now"})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>QUIZ<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class QuizView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        if id is None:
            stu_course = StudentCourse.objects.filter(
                user=request.user).values_list('stu_course', flat=True).first()
            showquestion = AddQuestion.objects.filter(course=stu_course)
            serializers = AddQuestionSerializer(showquestion, many=True)
            return Response({'data': serializers.data})
        showquestion = AddQuestion.objects.filter(course__id=id)
        serializers = AddQuestionSerializer(showquestion, many=True)
        return Response(serializers.data)

    def post(self, request):
        user = request.user
        question = request.data.get('question')
        ans = request.data.get('your_answer')
        serializers = AnswerSerialization(data=request.data)
        serializers.is_valid(raise_exception=True)
        stu_course = StudentCourse.objects.filter(
            user=request.user).values_list('stu_course', flat=True).first()
        showquestion = ShowQuestion.objects.filter(
            course=stu_course).values_list('question', flat=True)
        for i in showquestion:
            if i == question:
                questions = AddQuestion.objects.filter(
                    id=request.data.get('question')).first()
                duplicate = YourAnswer.objects.filter(
                    question=questions, user=request.user)
                if duplicate:
                    return Response({"message": "you are selecting duplicate question"})
                YourAnswer.objects.create(
                    user=user, question=questions, your_answer=ans)
                return Response({'data': serializers.data})
        return Response("you are already given the answert of this question or either you are selecting diffrent question id , please check and ")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>RESULT VIEW<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class ResultView(APIView):
    def get(self, request):
        selected_course = StudentCourse.objects.filter(
            user=request.user).values_list('stu_course', flat=True).first()
        rightanswer = ShowQuestion.objects.filter(
            course=selected_course).values('question', 'right_answer')
        youranswer = YourAnswer.objects.filter(
            user=request.user).values('question', 'your_answer')
        marks = 0
        stu_ans = YourAnswer.objects.filter(
            user=request.user).values('question_id', 'your_answer')
        for i in stu_ans:
            correct_ans = ShowQuestion.objects.filter(
                question__id=i['question_id']).first()
            if correct_ans.right_answer == i['your_answer']:
                marks += 1
            else:
                pass
        SubmitExam.objects.update_or_create(
            user=request.user, total_marks=marks)
        submit = SubmitExam.objects.all()
        serializers = SubmitExamSerialization(submit, many=True)
        return Response({'course': selected_course, 'rightanswer': rightanswer, 'youranswer': youranswer, 'data': serializers.data})