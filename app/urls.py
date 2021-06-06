from django.urls import path
from .views import ProfileApiView, RegisterView,LoginView

urlpatterns = [
    path('register',RegisterView.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('profile',ProfileApiView.as_view(),name="profile")
]
