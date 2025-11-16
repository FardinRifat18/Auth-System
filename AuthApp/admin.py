from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Teacher, Student, Course, Assignment, Submission

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'first_name', 'last_name')

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_staff')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'is_superuser')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('user_type', 'phone', 'date_of_birth', 'address', 'profile_picture', 'is_verified', 'otp')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('user_type', 'phone', 'email', 'first_name', 'last_name')
        }),
    )

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'department', 'qualification', 'experience', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'subject')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'class_name', 'section', 'guardian_name', 'is_active')
    list_filter = ('class_name', 'section', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'roll_number')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'credit_hours')
    list_filter = ('teacher__department', 'credit_hours')
    search_fields = ('name', 'code', 'teacher__user__username')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'due_date', 'total_marks')
    list_filter = ('course', 'teacher')
    search_fields = ('title', 'course__name')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'marks_obtained')
    list_filter = ('assignment__course', 'submitted_at')
    search_fields = ('student__user__username', 'assignment__title')

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)