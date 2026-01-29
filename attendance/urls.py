from django.urls import path
from . import views
from .views import login, signupStudent, studentProfile

urlpatterns = [
    path('scan/', views.scan_qr, name='scan_qr'),
    path('success/', views.attendance_success, name='attendance_success'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin/courses/', views.add_course, name='add_course'),
    path('admin/locations/', views.add_location, name='add_location'),

    path("signup/", signupStudent, name="signup"),
    path("login/", login, name="login"),
    path("student_profile", studentProfile, name="student_profile") 
]