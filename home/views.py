from email import message
from django.http.request import HttpHeaders
from django.shortcuts import render

from django.http import HttpResponse
import requests
import json
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from firebase_admin import messaging

def send_via_messaging(request):
    topic="Russia-Ukrain-Standoff"

    device = FCMDevice.objects.all().first()
    response = messaging.subscribe_to_topic(tokens=[device.registration_id], topic=topic)
    #response = messaging.unsubscribe_from_topic(tokens=[device.registration_id], topic="Russia-Ukrain-Standoff")

    notification = Message(notification=Notification(title="Russia-Ukrain Standoff", body="Russia-Ukrain War, Tables turned",image = "https://storage.googleapis.com/afs-prod/media/35fd8b00bc574708a0211005c98d4609/1000.jpeg"), topic=topic)
    response = messaging.send(notification)

    return HttpResponse('<h1 style="text-align: center;"> Notification Sent! to topic:</h1>')

def send_notification_to_devices(request):
    #Fetch devices we want to send notifications to, from FCMDevice model which comes with fcm_django package.
    #If no FCMDevices saved in db, goto admin panel and create new ones.

    device = FCMDevice.objects.all().first()
    device.send_message(Message(notification=Notification(title="Russia-Ukrain Standoff", body="Russia-Ukrain War, Tables turned",image = "https://storage.googleapis.com/afs-prod/media/35fd8b00bc574708a0211005c98d4609/1000.jpeg")))

    return HttpResponse('<h1 style="text-align: center;"> Notification Sent! </h1>')


def send_notification_to_topic(request):
    #Fetch devices we want to send notifications to, from FCMDevice model which comes with fcm_django package.
    #If no FCMDevices saved in db, goto admin panel and create new ones.

    #Subscribe devices to a topic
    device = FCMDevice.objects.all().first()
    device.handle_topic_subscription(should_subscribe = True, topic="Russia-Ukrain")

    # Send a message to the devices subscribed to the provided topic.
    message = Message(notification=Notification(title="Russia-Ukrain Standoff", body="Russia-Ukrain War, Tables turned",image = "https://storage.googleapis.com/afs-prod/media/35fd8b00bc574708a0211005c98d4609/1000.jpeg"))
    FCMDevice.send_topic_message(message=message,topic_name="Russia-Ukrain")

    return HttpResponse('<h1 style="text-align: center;"> Notification Sent! </h1>')


def index(request):
    return render(request , 'index.html')

def subscribe(request):
    return render(request , 'subscribe.html')

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js"); ' \
        '         const firebaseConfig = {'\
        '               apiKey: "AIzaSyBsavItP5j8wf5jKDOVpt6vI5wvbJ2lQBE", '\
        'authDomain: "push-notification-c52a5.firebaseapp.com",'\
        'projectId: "push-notification-c52a5",'\
        'storageBucket: "push-notification-c52a5.appspot.com",'\
        'messagingSenderId: "266172152466",'\
        'appId: "1:266172152466:web:cbceb2ce5073f0ec6c444b",'\
        'measurementId: "G-3P4JJWT9EN"'\
      '};'\
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")
