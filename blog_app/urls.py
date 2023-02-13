from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms  import *
urlpatterns = [
    path('home', home, name='home'),
    path('register',register,name='register'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('blog',blog,name='blog'),
    path('showblog/<int:pk>',detail_blog,name='detail_blog'),
    path('<int:pk>',edit_blog,name='edit_blog'),
    path('delete/<int:kp>',blog_delete,name='delete'),
    path('all_blog',all_blog,name='all_blog'),
    path("password_reset", password_reset_request, name="password_reset")
]
