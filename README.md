# django-push-notifications

A minimal Django app that implements Device models that can send messages through APNS and GCM.


The app implements four models: `GCMDevice`, `APNSDevice`, `WNSDevice` and `WebPushDevice`. 
Those models share the same attributes:

1. `name` (optional): A name for the device.
2. `active` (default True): A boolean that determines whether the device will be sent notifications.
3. `user` (optional): A foreign key to auth.User, if you wish to link the device to a specific user.
4. `device_id` (optional): A UUID for the device obtained from Android/iOS/Windows APIs, if you wish to uniquely identify it.
5. `registration_id` (required): The FCM/GCM registration id or the APNS token for the device.

The app also implements an admin panel, through which you can test single and bulk notifications. Select one or more FCM/GCM, APNS, WNS or WebPush devices and in the action dropdown, select "Send test message" or "Send test message in bulk", accordingly. Note that sending a non-bulk test message to more than one device will just iterate over the devices and send multiple single messages. UPDATE_ON_DUPLICATE_REG_ID: Transform create of an existing Device (based on registration id) into a update. See below Update of device with duplicate registration ID for more details.

### SetUp 
`$ pip install django-push-notifications`

Add this package in your Installed Apps in `settings.py` file
```
INSTALLED_APPS = [
    ...
    'push_notifications'
]
```
Install firebase admin.

`$ pip install firebase-admin`

Now login into your [google firebase console account]('https://console.firebase.google.com/u/0/) then select your `project`, then on your top left corner select `project overview` then select `project settings` now select `service account` then click on `Generate new private key`
this will download the json file for your project and save it 

Then create a json file in your project folder (wihtin the root folder).

```
{
    "type": "service_account",
    "project_id": "YOUR PROJECT ID",
    "private_key_id": "YOUR PRIVATE KEY ID",
    "private_key": "YOUR PRIVATE KEY",
    "client_email": "firebase-adminsdk@YOUR_ACCOUNT.iam.gserviceaccount.com",
    "client_id": "YOUR CLIENT ID",
    "auth_uri": "YOUR AUTH URI",
    "token_uri": "YOUR TOKEN URI",
    "auth_provider_x509_cert_url": "YOUR AUTH PROVIDER X509 CERT URL",
    "client_x509_cert_url": "YOUR CLIENT X509 CERT URL",
    "universe_domain": "googleapis.com"
  }
  
```

##### Create a GCM table and add the tokens into it

In order to send messages, we need to register our fcm tokens in the GCM table(as we are using token based procedure). For that we will be using the below code.
Here, the token we are passing is the token that we obtained from the firebase account during our project registration.

```
views.py

from push_notifications.models import GCMDevice
from django.http import HttpResponse

def update_notification_key(request, user_id):
    notification_token = request.data.get('notification_token', None)
    if notification_token:
        obj, created = GCMDevice.objects.get_or_create(registration_id=notification_token,         cloud_message_type="FCM", user_id=user_id)
        return HttpResponse('success')
    else:
        return HttpResponse('notification_token is misssing')
    
```

### Note

To migrate from legacy FCM APIs to HTTP v1, see [FCM docs here]('https://firebase.google.com/docs/cloud-messaging/migrate-v1').


Now, to use the firebase service, we need to initialize the app.
Add this in your `views.py` file

```
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("service_account.json")
firebase_admin.initialize_app(cred)


```
When you run the application, just incase if you encounter the error as 'app already exists', then re-write the above code as shown below.

```
import firebase_admin
from firebase_admin import credentials


if not firebase_admin._apps:
    cred = credentials.Certificate("service_account.json")
    firebase_admin.initialize_app(cred)

```


### Sending Messages
GCM have slightly different semantics. The app tries to offer a common interface for both when using the models.


###### Note
As the server key is deprecated by FCM legacy API and need to migrate it to HTTP v1, here I am using the token based push notifications for sending messages.


```
views.py


from push_notifications.models import GCMDevice
import firebase_admin
from firebase_admin import messaging
from django.http import HttpResponse

def notify_user(request, user_id):
    device = GCMDevice.objects.get(user_id=user_id)
    token = device.registration_id

    message = messaging.Message(
        data={
            "title": "your title",
            "body": "your body",
        },
        token=token
    )
    response = messaging.send(message)
    return HttpResponse('success')
```
