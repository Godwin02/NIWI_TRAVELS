from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('login/',views.login,name='login'),
    path('loginview/',views.loginview,name='loginview'),
    path('register/',views.register,name='register'),
    
    path('loginview/logout',views.log,name='logout'),
]