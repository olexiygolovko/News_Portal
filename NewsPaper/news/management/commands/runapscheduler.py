import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from news.models import *

logger = logging.getLogger(__name__)


def news_sender():
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


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            news_sender,

            # для проверки отправки временно задано время срабатывания каждые 10 секунд
            trigger=CronTrigger(second="*/30"),

            # отправляем письма подписчикам в понедельник в 8 утра
            # trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),

            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="news_sender",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена работка 'news_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="19", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить,
            # либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Задачник запущен")
            print('Задачник запущен')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Задачник остановлен")
            scheduler.shutdown()
            print('Задачник остановлен')
            logger.info("Задачник остановлен успешно!")
