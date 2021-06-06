"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from main.views import home, signup, report, report_msg, report_user, livechat, api_lc_messages, api_lc_add, \
    api_lc_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('livechat', livechat, name="livechat"),
    path('api/lc/messages', api_lc_messages, name="api lc messages"),
    path('api/lc/add', api_lc_add, name="api lc add"),
    path('api/lc/delete', api_lc_delete, name="api lc delete"),
    path('report/<int:year>/<int:month>/<int:day>', report, name="report"),
    path('report/<int:year>/<int:month>/<int:day>/<str:user>', report_user, name="report_user"),
    path('report/<int:year>/<int:month>/<int:day>/<str:user>/<int:msg_id>', report_msg, name="report_msg"),
    path('accounts/signup', signup, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),
]
