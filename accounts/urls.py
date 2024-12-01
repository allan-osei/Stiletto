from django.urls import path, reverse_lazy
from .views import signup, log_in, log_out
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('login/', log_in, name='login'),
    path('sign-out/', log_out, name='sign-out'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password-reset/password_reset_form.html',
        email_template_name='password-reset/password_reset_email.html',
        subject_template_name='password-reset/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password-reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password-reset/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password-reset/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password-reset-confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password-reset/password_reset_complete.html'
    ), name='password_reset_complete'),
]