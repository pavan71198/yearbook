"""yearbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from social_django import urls as social_django_urls
from students import views as student_views

urlpatterns = [
    path('', student_views.home, name='home'),
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', student_views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('oauth/', include(social_django_urls, namespace='social')),
    path('<username>/', student_views.profile, name='profile'),
    path('<username>/add_testimonial/', student_views.add_testimonial, name='add_testimonial')
]
