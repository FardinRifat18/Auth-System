#urls,py

from django.urls import path
from . views import *
from django.conf import settings
from django.conf.urls.static import static
from django.core.mail import send_mail


urlpatterns = [
    path('', home, name='home'),                      # Home page
    path('register/', register_view, name='register'),# Registration
    path('login/', login_view, name='login'),         # Login
    path('dashboard/', dashboard, name='dashboard'), # Dashboard
    path('logout/', logout_view, name='logout'),      # Logout
    path('verify-otp/', verify_otp_view, name='verify_otp'),  # OTP verification
    path('forget/', forget_password_view, name='forget_password'), # Forget password
    path('reset-password/', reset_password_view, name='reset_password'), # Reset password
    path('send-email/', send_test_email, name='send_email'),
    path('teacher/', teacher, name='teacher'),
    
]