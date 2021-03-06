"""database_do URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from app01 import  views

urlpatterns = [
    path('',views.login),#默认跳转到登录页面
    path('admin/', admin.site.urls),
    path('classes/',views.classes),
    path('add/',views.add),
    path('delete/',views.delete),
    path('edit/',views.edit),
    path('student_manage/',views.student_manage),
    path('student_add/',views.student_add),
    path('student_edit/',views.student_edit),
    path('modal_add_class/',views.modal_add_class),
    path('modal_del_class/',views.modal_del_class),
    path('modal_edit_class/', views.modal_edit_class),
    path('modal_add_student/', views.modal_add_student),
    path('modal_edit_student/', views.modal_edit_student),
    path('modal_del_student/',views.modal_del_student),
    path('teacher/',views.teacher),
    path('add_teacher/',views.add_teacher),
    path('edit_teacher/',views.edit_teacher),
    path('layout/',views.layout),
    path('login/', views.login),
    path('select_course/',views.select_course),
    path('del_my_course/',views.del_my_course),
    path('add_my_course/',views.add_my_course),
    path('del_teacher/',views.del_teacher),

]
