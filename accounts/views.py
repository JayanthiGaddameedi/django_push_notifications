from django.shortcuts import render
from django.http import HttpResponse

import firebase_admin
from firebase_admin import credentials, messaging

# Create your views here.

cred = credentials.Certificate("service_account.json")
firebase_admin.initialize_app(cred)

token = 'token' # this is the fcm token that you get when you create a new project in firebase
  
message = messaging.Message(
    data={
        "notification_type": '0',
        "click_action": "FLUTTER_NOTIFICATION_CLICK",  # if your app runs on Android using flutter
        "title": "your title",
        "body": "your body",
    },
    token=token
)
response = messaging.send(message)
print('Successfully sent message:', response)



def notify_users(request):
    message = messaging.Message(
        data={
            "notification_type": '0',
            "click_action": "FLUTTER_NOTIFICATION_CLICK",  # if your app runs on Android using flutter
            "title": "your title",
            "body": "your body",
        },
        token=token
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)
    return HttpResponse('Successfully sent message')
