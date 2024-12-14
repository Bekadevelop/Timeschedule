import json
from pywebpush import webpush, WebPushException
from django.conf import settings
from .models import UserSubscription

def push_notification(user_id, message):
    """
    Отправляет push-уведомление подписанному пользователю.

    :param user_id: ID пользователя
    :param message: Текст уведомления (словарь с 'title' и 'body')
    """
    user_subscriptions = UserSubscription.objects.filter(user_id=user_id)
    for subscription in user_subscriptions:
        try:
            webpush(
                subscription_info=json.loads(subscription.subscription),
                data=json.dumps(message),
                vapid_private_key='./private_key.pem',
                vapid_claims={
                    'sub': f'mailto:{settings.ADMIN_EMAIL}',
                },
                ttl=60
            )
            print(f"Уведомление отправлено пользователю с ID {user_id}.")
        except WebPushException as ex:
            print(f"Ошибка отправки уведомления пользователю с ID {user_id}: {repr(ex)}")
