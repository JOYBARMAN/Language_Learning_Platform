"""Url mapping for authentication api"""

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from authentications.rest.views.authentications import (
    RegistrationView,
    LoginView,
    ActiveAccountView,
    ChangePasswordView,
    PasswordResetMailView,
    PasswordResetView,
)


urlpatterns = [
    path("/sign-up", RegistrationView.as_view(), name="registration"),
    path("/token", LoginView.as_view(), name="token"),
    path("/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/active-account", ActiveAccountView.as_view(), name="activate-account"),
    path("/change-password", ChangePasswordView.as_view(), name="change-password"),
    path(
        "/password-reset-mail",
        PasswordResetMailView.as_view(),
        name="password-reset-mail",
    ),
    path(
        "/password-reset/<uid>/<token>",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
]
