"""pushnoti URL Configuration

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
from django.urls import path
from home.views import *

urlpatterns = [

    path('' , index),
    path('subscribe' , subscribe),

    path('send_via_messaging/' , send_via_messaging),

    path('send_to_devices/' , send_notification_to_devices),
    path('publish_to_topic/' , send_notification_to_topic),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
    path('test_cache' , test_cache),

    path('admin/', admin.site.urls),
]
