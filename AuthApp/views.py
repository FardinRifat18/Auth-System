# views.py 


from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
import random
from django.core.mail import send_mail 
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

#
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib import messages
# from django.http import HttpResponseForbidden
# from .models import CustomUser, Teacher, Student, Course, Assignment, Submission
# from .forms import CustomUserCreationForm, TeacherProfileForm, StudentProfileForm

# Home page
def home(request):
    return render(request, 'home.html')


# Registration
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        #image = request.FILES.get("image")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")
            

        otp_code = f"{random.randint(000000, 999999)}"
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=confirm_password,
            #image=image,
            otp=otp_code,
            
        )
        user.save()

        akij(otp_code, email)

        messages.success(request, f"Account created successfully!")
        return redirect("verify_otp")

    return render(request, "reg.html")



def akij(otp_code, email):
    email = email
    otp_code = otp_code
    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp_code}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return HttpResponse("Email sent successfully ✅")


# OTP Verification
def verify_otp_view(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        try:
            user = CustomUser.objects.get(otp=otp)
            user.is_verified = True
            user.otp = ""
            user.save()
            messages.success(request, "OTP verified successfully. You can now log in.")
            return redirect("login")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_otp")
    return render(request, "otp.html")



# Login
def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        # Allow login with email or username
        try:
            user_obj = CustomUser.objects.get(email=username_or_email)
            username = user_obj.username
        except CustomUser.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_verified:
                messages.error(request, "Please verify your account first.")
                return redirect("login")

            if user.is_active==True and user.is_staff==True and user.is_superuser==True and user.is_student==False and user.is_teacher==False and user.is_admin==True:
                login(request, user)
                messages.success(request, f"Welcome Admin {user.username}!")
                return redirect("admin")  # Replace with your admin dashboard URL

            elif user.is_active==True and user.is_staff==False and user.is_superuser==False and user.is_student==True and user.is_teacher==False and user.is_admin==True:
                login(request, user)
                messages.success(request, f"Welcome Admin {user.username}!")
                return redirect("home")  # Replace with your admin dashboard URL
            
            elif user.is_active==True and user.is_staff==False and user.is_superuser==False and user.is_student==False and user.is_teacher==True and user.is_admin==True:
                login(request, user)
                messages.success(request, f"Welcome Admin {user.username}!")
                return redirect("teacher")  # Replace with your admin dashboard URL
            

            if user.is_verified:
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Please verify your account first.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


@login_required
def dashboard(request):
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)


# Logout
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")


# ---------------------- FORGOT PASSWORD SYSTEM ----------------------

# Step 1: Enter email to send OTP
def forget_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            # Generate reset OTP
            otp_code = str(random.randint(000000, 999999))
            user.otp = otp_code
            user.save()
            messages.success(request, f"Reset OTP sent! Your OTP is {otp_code}")  # For demo, display OTP
            return redirect('reset_password')
        except CustomUser.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('forget_password')
    return render(request, "forget.html")


# Step 2: Reset password using OTP
def reset_password_view(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")

        try:
            user = CustomUser.objects.get(otp=otp)
            user.set_password(new_password)
            user.otp = ""
            user.save()
            messages.success(request, "Password reset successfully! You can now log in.")
            return redirect("login")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid OTP.")
            return redirect("reset_password")

    return render(request, "reset_password.html")






def send_test_email(request):
    subject = "Test Email from Django"
    message = "Hello! This is a test email sent from Django."
    recipient_list = ["recipient@example.com"]  # Replace with actual recipient

    try:
        send_mail(
            subject,
            message,
            None,                # Uses DEFAULT_FROM_EMAIL
            recipient_list,
            fail_silently=False,
        )
        messages.success(request, "Email sent successfully!")
    except Exception as e:
        messages.error(request, f"Failed to send email: {e}")

    return redirect("home")

def teacher(request):
    return render(request, 'teacher.html')





#
# Utility functions
# def is_admin(user):
#     return user.is_authenticated and user.user_type == 'admin'

# def is_teacher(user):
#     return user.is_authenticated and user.user_type == 'teacher'

# def is_student(user):
#     return user.is_authenticated and user.user_type == 'student'

# # Authentication Views
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_verified = True  # For demo, auto-verify
#             user.save()
            
#             # Create profile based on user type
#             if user.user_type == 'teacher':
#                 Teacher.objects.create(user=user)
#             elif user.user_type == 'student':
#                 Student.objects.create(user=user)
            
#             messages.success(request, 'Registration successful! Please login.')
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, 'reg.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             if user.is_verified:
#                 login(request, user)
#                 messages.success(request, f'Welcome back, {user.username}!')
                
#                 # Redirect based on user type
#                 if user.user_type == 'admin':
#                     return redirect('admin_dashboard')
#                 elif user.user_type == 'teacher':
#                     return redirect('teacher_dashboard')
#                 elif user.user_type == 'student':
#                     return redirect('student_dashboard')
#             else:
#                 messages.error(request, 'Please verify your account first.')
#         else:
#             messages.error(request, 'Invalid credentials')
    
#     return render(request, 'login.html')

# def logout_view(request):
#     logout(request)
#     messages.success(request, 'You have been logged out successfully.')
#     return redirect('home')

# # Dashboard Views
# @login_required
# def admin_dashboard(request):
#     if not is_admin(request.user):
#         return HttpResponseForbidden("Access denied")
    
#     total_teachers = Teacher.objects.count()
#     total_students = Student.objects.count()
#     total_courses = Course.objects.count()
    
#     context = {
#         'total_teachers': total_teachers,
#         'total_students': total_students,
#         'total_courses': total_courses,
#         'recent_teachers': Teacher.objects.all()[:5],
#         'recent_students': Student.objects.all()[:5],
#     }
#     return render(request, 'admin.html', context)

# @login_required
# def teacher_dashboard(request):
#     if not is_teacher(request.user):
#         return HttpResponseForbidden("Access denied")
    
#     try:
#         teacher = Teacher.objects.get(user=request.user)
#         courses = Course.objects.filter(teacher=teacher)
#         assignments = Assignment.objects.filter(teacher=teacher)
        
#         context = {
#             'teacher': teacher,
#             'courses': courses,
#             'assignments': assignments,
#             'total_courses': courses.count(),
#             'total_assignments': assignments.count(),
#         }
#         return render(request, 'teacher.html', context)
#     except Teacher.DoesNotExist:
#         messages.error(request, 'Teacher profile not found.')
#         return redirect('login')

# @login_required
# def student_dashboard(request):
#     if not is_student(request.user):
#         return HttpResponseForbidden("Access denied")
    
#     try:
#         student = Student.objects.get(user=request.user)
#         courses = student.courses.all()
#         submissions = Submission.objects.filter(student=student)
        
#         context = {
#             'student': student,
#             'courses': courses,
#             'submissions': submissions,
#             'total_courses': courses.count(),
#             'total_submissions': submissions.count(),
#         }
#         return render(request, 'student.html', context)
#     except Student.DoesNotExist:
#         messages.error(request, 'Student profile not found.')
#         return redirect('login')

# # Profile Management
# @login_required
# def profile_view(request):
#     user = request.user
#     context = {'user': user}
    
#     try:
#         if user.user_type == 'teacher':
#             context['teacher'] = Teacher.objects.get(user=user)
#         elif user.user_type == 'student':
#             context['student'] = Student.objects.get(user=user)
#     except (Teacher.DoesNotExist, Student.DoesNotExist):
#         pass
    
#     return render(request, 'profile.html', context)

# @login_required
# def edit_profile_view(request):
#     user = request.user
    
#     if request.method == 'POST':
#         user.first_name = request.POST.get('first_name', '')
#         user.last_name = request.POST.get('last_name', '')
#         user.email = request.POST.get('email', '')
#         user.phone = request.POST.get('phone', '')
#         user.save()
        
#         messages.success(request, 'Profile updated successfully!')
#         return redirect('profile')
    
#     return render(request, 'edit_profile.html', {'user': user})
