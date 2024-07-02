from django.urls import path
from . import views

urlpatterns = [
    path('', views.UnderWorkView.as_view(), name='under-work'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-email/', views.email_verification, name='verify-email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'), 
    path('about/', views.AboutView.as_view(), name='about'),
    path('registration/', views.register, name='registration'),  
    path('under-work/', views.UnderWorkView.as_view(), name='under-work'),
]