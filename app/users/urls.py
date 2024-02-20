from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("delete/", views.DeleteView.as_view(), name="delete"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("email/verify/token/<str:token>/", views.EmailVerifyView.as_view(), name="email_verify"),
    path("email/verify/resend/", views.EmailVerifyResendView.as_view(), name="email_verify_resend"),
    path("email/change/", views.EmailChangeView.as_view(), name="email_change"),
    path("password/change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
