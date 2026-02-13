from django.urls import path
from . import views
<<<<<<< HEAD
=======
from .views import login
>>>>>>> 425f204d3c70eb974a33a8f3532e3268655b9eb4

urlpatterns = [
    path('scan/', views.scan_qr, name='scan_qr'),
    path('success/', views.attendance_success, name='attendance_success'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin/courses/', views.add_course, name='add_course'),
    path('admin/locations/', views.add_location, name='add_location'),
    
    path('register/', views.student_register, name='student_register'),
    path("logout/", views.logout_view, name="logout"),

<<<<<<< HEAD
]
=======
    path("student/signup/", views.student_signup, name="student_signup"),
    path("student/login/", views.student_login, name="student_login"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    ]
>>>>>>> 425f204d3c70eb974a33a8f3532e3268655b9eb4
