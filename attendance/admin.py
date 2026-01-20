from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, QRCode, Attendance, OrganizationLocation

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name']
    list_filter = ['user_type', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number')}),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_active', 'created_at']
    list_filter = ['is_active']
    readonly_fields = ['qr_image']

@admin.register(OrganizationLocation)
class OrganizationLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'radius_meters', 'is_active']
    list_filter = ['is_active']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'check_in_time', 'is_valid']
    list_filter = ['is_valid', 'course', 'user__user_type', 'check_in_time']
    search_fields = ['user__username', 'course__name']
    date_hierarchy = 'check_in_time'