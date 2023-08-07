from django.urls import path
from .views import *
from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

app_name ="user"

urlpatterns =[
    path('create-profile/', CreateProfileView.as_view(), name="create_profile"),
    path('register/', signup_view, name="sign_up"),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', logout, name="logout"),
    path('reset-password/', PasswordResetView.as_view(
        template_name='registrations/password_reset.html',
        success_url=reverse_lazy('resume:password_reset_done')
    ), name="password_reset"),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='registrations/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/(<uidb64>)-(<token>)/', PasswordResetConfirmView.as_view(
        template_name='registrations/password_reset_confirm.html',
        success_url=reverse_lazy('resume:password_reset_complete')
    ), name="password_reset_confirm"),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='registrations/password_reset_complete.html'),
         name="password_reset_complete"),
    path('user/<int:pk>/user_edit/', user_edit, name="user_edit"),
    path('user/profile_edit/', profile_edit, name="profile_edit"),
    path('user/<int:pk>/', UserDetailView.as_view(), name="user_detail"),
    path('user/change-password/', change_password, name="change_password"),
]