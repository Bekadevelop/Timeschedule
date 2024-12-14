from django.conf import settings

def notification_key(request):
    return {
        'NOTIFICATION_KEY': settings.NOTIFICATION_KEY
    }
