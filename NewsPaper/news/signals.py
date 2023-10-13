from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# the signal to which this function will react is passed to the decorator as the first argument, and to the senders it is necessary
# also pass the model

@receiver(m2m_changed, sender=PostCategory)
def notify_subscriber(sender, instance, **kwargs):
    for cat in instance.postCategory.all():
        subscribers = Subscribers.objects.filter(category=cat)
        for person in subscribers:
            html_content = render_to_string(
                'news/subscription_letter.html',
                {
                    'post': instance,
                    'person': person,
                    'cat': cat,
                }
            )
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text,
                from_email='ogolovko92@yandex.ru',
                to=[person.subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()
