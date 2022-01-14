from django.urls import path, include
from .views import ForgotPasswordView, LogoutView, RegisterView, LoginView, ResetPasswordView, UserView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('forgot/', ForgotPasswordView.as_view()),
    path('reset/', ResetPasswordView.as_view())
]
