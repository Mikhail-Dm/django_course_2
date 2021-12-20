from django.conf import settings
from django.core.mail import send_mail

from django.urls import reverse
from django.template.loader import render_to_string


def send_verify_email(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activate_key])
    full_link = f'{settings.BASE_URL}{verify_link}'

    message = f'Your activation url: {full_link}'
    # message = render_to_string('authapp/email/register_message.html', {'full_link': full_link})

    return send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )