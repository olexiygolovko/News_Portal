from datetime import datetime

from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import *
# from .signals import notify_subscriber


@shared_task
def weekly_post_mail():
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = datetime.now().isocalendar()[1] - 2
        for news in Post.objects.filter(postCategory=category.id, dateCreation__week=week_number_last).values(
                                                                                    'pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'postCategory__name'):

            date_format = news.get('dateCreation').strftime("%d/%m/%Y")
            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Категория: {news.get("postCategory__name")}, Дата создания: {date_format}')

            news_from_each_category.append(new)

        subscribers = category.subscriber.all()

        for subscriber in subscribers:
            html_content = render_to_string(
                'news/subscription_letter_weekly.html', {'user': subscriber,
                                                    'text': news_from_each_category,
                                                    'name': category.name,
                                                    'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}, новые статьи за прошлую неделю в вашем разделе!',
                from_email='ogolovko92@yandex.ru',
                to=[subscriber.email]
            )

            if news_from_each_category:
                msg.attach_alternative(html_content, 'text/html')

                msg.send()



# @shared_task()
# def new_post_mail_notification():
#     notify_subscriber()
#     print("new post notification have been sent from celery...")
