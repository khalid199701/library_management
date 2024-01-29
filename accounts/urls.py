from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    # path('user_login/', views.user_login, name='user_login'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    # path('logout/', views.user_logout, name='user_logout'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/edit', views.EditProfile.as_view(), name='edit_profile'),
]