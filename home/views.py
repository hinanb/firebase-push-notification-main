from django.shortcuts import render

from django.http import HttpResponse
import requests
import json
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from firebase_admin import messaging
from pyfcm import FCMNotification

def initialize_fcm_package():
    #server key for auth
    push_service = FCMNotification(api_key='AAAAPfkYupI:APA91bHxokzTLn_5rkdiZob3dEweZoYMOVUjgE8NmSoZTlxw-v03kKaVy9vn69gnAHb1BGybd1sxofmBnyFkVzYSOW_qUu3HmMU6fsv-bZMx8DHvFGxWqGkcs9Zg8aPMrDlF_mwY_Ueg')
    return push_service, {'**fcm_options**': {
        'analytics_label': 'notification-label'}}, 'dumuBg2UKLwtSx0v2benHk:APA91bG1pGd-AR0CLuTv_NPXiBM7SnskIG__XOkJUW7Pt8IzmsbJqEf-ztLpnYcogMO6wq0GGCKxr-CMiLdpNr6vtiySLymXNPAd58mv__lcAR28eT0dupAm9axvf1YvGhM0BPtxGmJB'


def send_via_fcm_package_single_device(request):

    #single device push notification
    message_title = 'BBC: Russia-Ukrain War'
    message_body = 'Russia-Ukrain War takes a new turn'

    push_service, extra_kwargs, registration_id  = initialize_fcm_package()
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, extra_kwargs=extra_kwargs)
    return HttpResponse('Notification Sent')

def send_via_fcm_multiple_devices(request):

    # Send to multiple devices by passing a list of ids.
    message_title = 'BBC: Russia-Ukrain War'
    message_body = 'Russia-Ukrain War takes a new turn'
    push_service, extra_kwargs, registration_id  = initialize_fcm_package()
    registration_ids = ['dumuBg2UKLwtSx0v2benHk:APA91bEvcmZCcu-AAeD2-5LuqaikKqrK-w04RSSU1akp2DTEMcUBWiji7W014cd8dtuAy4xb44u40mIMur2Li8-DLIhR-9HuyZar2l5f5e8Otvm7DAaCFaAVhF2hiFAQdbEzXwGVel8e'
                        ,'dumuBg2UKLwtSx0v2benHk:APA91bEvcmZCcuujjas', registration_id]

    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, extra_kwargs=extra_kwargs )

    return HttpResponse('Notification sent to multiple devices')

def fcm_package_topic_handling(request):

    push_service, extra_kwargs, registration_id  = initialize_fcm_package()
    topic_name = 'Sports'

    #Topic subscription
    subscribed = push_service.subscribe_registration_ids_to_topic([registration_id], topic_name)
    # returns True if successful, raises error if unsuccessful
    print(subscribed)

    # Send a message to devices subscribed to a topic.
    push_service.notify_topic_subscribers(topic_name=topic_name, message_body='hi', extra_kwargs=extra_kwargs)

    #Topic UnSubscription
    unsubscribed = push_service.unsubscribe_registration_ids_from_topic([registration_id], topic_name)
    print(unsubscribed)

    # Send a message to devices subscribed to a topic.
    push_service.notify_topic_subscribers(topic_name=topic_name, message_body='hi')

def send_via_requests(request):
    _, _, registration_id  = initialize_fcm_package()

    data = {
    'to':registration_id,
    'notification' : {
    'body' : 'Russias special military action takes a new turn.',
    'OrganizationId':'2',
    'content_available' : True,
    'priority' : 'high',
    'subtitle':'Elementary School',
    'Title':'Russia-Ukrain War, Tables turned',
    'image' : 'https://storage.googleapis.com/afs-prod/media/35fd8b00bc574708a0211005c98d4609/1000.jpeg',
    'icon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Associated_Press_logo_2012.svg/220px-Associated_Press_logo_2012.svg.png'

    },
    'data' : {
    'priority' : 'high',
    'sound':'app_sound.wav',
    'content_available' : True,
    'bodyText' : 'New Announcement assigned',
    'organization' :'Elementary school'
    }
    }

    headers = {
        'Content-Type':'application/json',
        'Authorization': 'key=AAAAPfkYupI:APA91bHxokzTLn_5rkdiZob3dEweZoYMOVUjgE8NmSoZTlxw-v03kKaVy9vn69gnAHb1BGybd1sxofmBnyFkVzYSOW_qUu3HmMU6fsv-bZMx8DHvFGxWqGkcs9Zg8aPMrDlF_mwY_Ueg'}

    requests.post('https://fcm.googleapis.com/fcm/send', data= json.dumps(data), headers=headers)

    return HttpResponse('Sent')


def send_via_messaging(request):
    topic='Russia-Ukrain-Standoff'

    device = FCMDevice.objects.all().first()
    response = messaging.subscribe_to_topic(tokens=[device.registration_id], topic=topic)
    #response = messaging.unsubscribe_from_topic(tokens=[device.registration_id], topic="Russia-Ukrain-Standoff")

    notification = Message(notification=Notification(title='Russia-Ukrain Standoff', body='Russia-Ukrain War, Tables turned',image = 'https://storage.googleapis.com/afs-prod/media/35fd8b00bc574708a0211005c98d4609/1000.jpeg'), topic=topic)
    response = messaging.send(notification)

    return HttpResponse('<h1 style="text-align: center;"> Notification Sent! to topic:</h1>')

def send_notification_to_devices(request):
    #Fetch devices we want to send notifications to, from FCMDevice model which comes with fcm_django package.
    #If no FCMDevices saved in db, goto admin panel and create new ones.

    device = FCMDevice.objects.all().first()
    device.send_message(Message(notification=Notification(title='Russia-Ukrain Standoff', body='Russia-Ukrain War, Tables turned',image = 'https://storage.googleapis.com/afs-prod/media/35fd8b00bc574708a0211005c98d4609/1000.jpeg')))

    return HttpResponse('<h1 style="text-align: center;"> Notification Sent! </h1>')


def send_notification_to_topic(request):
    #Fetch devices we want to send notifications to, from FCMDevice model which comes with fcm_django package.
    #If no FCMDevices saved in db, goto admin panel and create new ones.

    #Subscribe devices to a topic
    device = FCMDevice.objects.all().first()
    device.handle_topic_subscription(should_subscribe = True, topic='Russia-Ukrain')

    # Send a message to the devices subscribed to the provided topic.
    message = Message(notification=Notification(title='Russia-Ukrain Standoff', body='Russia-Ukrain War, Tables turned',image = 'https://storage.googleapis.com/afs-prod/media/35fd8b00bc574708a0211005c98d4609/1000.jpeg'))
    FCMDevice.send_topic_message(message=message,topic_name='Russia-Ukrain')

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

    return HttpResponse(data,content_type='text/javascript')
