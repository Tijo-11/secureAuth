from django.urls import path
from .views import RegisterView, LoginView, RefreshView, GetUser, LogoutView, CsrfTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('user/', GetUser.as_view(), name='user'),
    path('csrf/', CsrfTokenView.as_view(), name='csrf-token'),
]

#name is required for running test