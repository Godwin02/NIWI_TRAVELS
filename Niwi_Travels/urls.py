from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('home/',views.index,name='home'),
    path('log/',views.login,name='log'),
    path('loginview/',views.loginview,name='loginview'),
    path('register/',views.register,name='register'),
    path('driver/',views.dri,name='driver'),

    path('accounts/login/',views.login,name='login'),
    
    path('logout/',views.logo,name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]