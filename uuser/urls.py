from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('student/', views.student_page, name='student_page'),
    path('teacher/', views.teacher_page, name='teacher_page'),
    path('save-subscription/', views.save_subscription, name='save_subscription'),
]

from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns += [
    path('password_reset/', PasswordResetView.as_view(template_name='uuser/password_reset.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='uuser/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='uuser/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='uuser/password_reset_complete.html'), name='password_reset_complete'),
    path('schedule/', views.schedule_view, name='schedule'),
]
