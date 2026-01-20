from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta
from geopy.distance import geodesic
from .models import User, Course, QRCode, Attendance, OrganizationLocation

def verify_location(latitude, longitude):
    """Verify if user is within organization premises"""
    locations = OrganizationLocation.objects.filter(is_active=True)
    
    for location in locations:
        org_coords = (location.latitude, location.longitude)
        user_coords = (latitude, longitude)
        distance = geodesic(org_coords, user_coords).meters
        
        if distance <= location.radius_meters:
            return True
    
    return False

@login_required
def scan_qr(request):
    """Main QR scanning page"""
    courses = Course.objects.filter(is_active=True)
    
    if request.method == 'POST':
        qr_code_value = request.POST.get('qr_code')
        course_id = request.POST.get('course')
        latitude = float(request.POST.get('latitude', 0))
        longitude = float(request.POST.get('longitude', 0))
        
        # Verify location
        if not verify_location(latitude, longitude):
            messages.error(request, 'You must be within the organization premises to sign in.')
            return redirect('scan_qr')
        
        # Verify QR code
        try:
            qr_code = QRCode.objects.get(code=qr_code_value, is_active=True)
        except QRCode.DoesNotExist:
            messages.error(request, 'Invalid QR code.')
            return redirect('scan_qr')
        
        # Get course
        course = get_object_or_404(Course, id=course_id)
        
        # Check if already signed in today
        today = timezone.now().date()
        existing_attendance = Attendance.objects.filter(
            user=request.user,
            course=course,
            check_in_time__date=today
        ).first()
        
        if existing_attendance:
            messages.warning(request, f'You have already signed in for {course.name} today.')
            return redirect('scan_qr')
        
        # Create attendance record
        Attendance.objects.create(
            user=request.user,
            course=course,
            latitude=latitude,
            longitude=longitude,
            qr_code=qr_code,
            is_valid=True
        )
        
        messages.success(request, f'Successfully signed in for {course.name}!')
        return redirect('attendance_success')
    
    return render(request, 'attendance/scan.html', {'courses': courses})

@login_required
def attendance_success(request):
    """Success page after signing in"""
    return render(request, 'attendance/success.html')

@login_required
def admin_dashboard(request):
    """Admin dashboard for viewing attendance"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('scan_qr')
    
    # Get filter parameters
    date_filter = request.GET.get('date', timezone.now().date())
    course_filter = request.GET.get('course', '')
    user_type_filter = request.GET.get('user_type', '')
    
    # Build query
    attendances = Attendance.objects.select_related('user', 'course')
    
    if date_filter:
        attendances = attendances.filter(check_in_time__date=date_filter)
    
    if course_filter:
        attendances = attendances.filter(course_id=course_filter)
    
    if user_type_filter:
        attendances = attendances.filter(user__user_type=user_type_filter)
    
    # Statistics
    total_today = Attendance.objects.filter(
        check_in_time__date=timezone.now().date()
    ).count()
    
    students_today = Attendance.objects.filter(
        check_in_time__date=timezone.now().date(),
        user__user_type='student'
    ).count()
    
    tutors_today = Attendance.objects.filter(
        check_in_time__date=timezone.now().date(),
        user__user_type='tutor'
    ).count()
    
    courses = Course.objects.filter(is_active=True)
    
    context = {
        'attendances': attendances,
        'total_today': total_today,
        'students_today': students_today,
        'tutors_today': tutors_today,
        'courses': courses,
        'date_filter': date_filter,
        'course_filter': course_filter,
        'user_type_filter': user_type_filter,
    }
    
    return render(request, 'attendance/admin_dashboard.html', context)










from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, OrganizationLocation


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'admin':
            messages.error(request, "Access denied.")
            return redirect('scan_qr')
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


@admin_required
def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')

        if Course.objects.filter(code=code).exists():
            messages.error(request, "Course code already exists.")
            return redirect('add_course')

        Course.objects.create(
            name=name,
            code=code,
            description=description
        )

        messages.success(request, "Course added successfully.")
        return redirect('add_course')

    courses = Course.objects.all()
    return render(request, 'attendance/add_course.html', {'courses': courses})


@admin_required
def add_location(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        radius = request.POST.get('radius')

        OrganizationLocation.objects.create(
            name=name,
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius
        )

        messages.success(request, "Location added successfully.")
        return redirect('add_location')

    locations = OrganizationLocation.objects.all()
    return render(request, 'attendance/add_location.html', {'locations': locations})







from django.contrib.auth import login
from django.shortcuts import redirect


@login_required
def post_login_redirect(request):
    if request.user.user_type == 'admin':
        return redirect('admin_dashboard')
    return redirect('scan_qr')
