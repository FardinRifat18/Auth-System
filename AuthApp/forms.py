from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Teacher, Student

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_verified = True  # Auto-verify for demo
        
        if commit:
            user.save()
            # Create profile based on user type
            if user.user_type == 'teacher':
                Teacher.objects.create(user=user)
            elif user.user_type == 'student':
                Student.objects.create(user=user)
        
        return user

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('subject', 'department', 'qualification', 'experience', 'salary')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_number', 'class_name', 'section', 'guardian_name', 'guardian_phone')