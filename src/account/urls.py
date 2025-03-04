from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Register routes
    path('signup/', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),

    # Login routes
    path('signin/', views.signin_view, name='signin'),

    # Logout route
    path('logout/', views.signout_view, name='logout'),

    # Pasword reset
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="auth/password_reset/password_reset_form.html"
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset/password_reset_done.html"
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset/password_reset_confirm.html"
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset/password_reset_complete.html"
        ),
        name='password_reset_complete'
    ),

    # Password change
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name="auth/password_change_form.html",
            success_url=reverse_lazy('profile')
        ),
        name='password_change'
    ),
]
