from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.urls import reverse

from users.models import User


def set_verify_token_and_send_mail(new_user):
    now = datetime.now(pytz.timezone(settings.TIME_ZONE))
    new_user.is_active = False
    new_user.verify_token = User.objects.make_random_password(length=20)
    new_user.verify_token_expired = now + timedelta(hours=72)
    new_user.save()

    link_to_verify = reverse('users:verify_email', args=[new_user.verify_token])
    send_mail(
        subject='Подтвердите почту для сервиса рассылки',
        message=f'http://localhost:8000{link_to_verify}',
        recipient_list=[new_user.email],
        from_email=settings.EMAIL_HOST_USER
    )


def generate_password_and_end_mail(user):
    new_password = User.objects.make_random_password(length=12)
    user.new_password = make_password(new_password)
    user.save()
    send_mail(
        subject='Новый пароль',
        message=f'{new_password}',
        recipient_list=[user.email],
        from_email=settings.EMAIL_HOST_USER
    )
