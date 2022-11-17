"""courses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/' ,QuizView.as_view()),
    path('quiz/<int:id>/' ,QuizView.as_view()),
    path('studentregistration/',UserRegistration.as_view(), name="studentregistration" ),
    path('studentlogin/',UserLogin.as_view(), name="studentlogin" ),
    path('submit/',SubmitView.as_view(), name="submit"),
    path('courseview/' , CourseView.as_view() , name='course')

]
