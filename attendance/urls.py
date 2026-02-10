from django.urls import path
from . import views
from .views import login

urlpatterns = [
    path('scan/', views.scan_qr, name='scan_qr'),
    path('success/', views.attendance_success, name='attendance_success'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin/courses/', views.add_course, name='add_course'),
    path('admin/locations/', views.add_location, name='add_location'),

    path("student/signup/", views.student_signup, name="student_signup"),
    path("student/login/", views.student_login, name="student_login"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    ]