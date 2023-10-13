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
                   f'Category: {news.get("postCategory__name")}, Date of creation:{date_format}')

            news_from_each_category.append(new)

        subscribers = category.subscriber.all()

        for subscriber in subscribers:
            html_content = render_to_string(
                'news/subscription_letter_weekly.html', {'user': subscriber,
                                                    'text': news_from_each_category,
                                                    'name': category.name,
                                                    'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Hello, {subscriber.username}, new articles for last week in your section!',
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

        # adding work to our problem book
        scheduler.add_job(
            news_sender,

            # to check sending, the response time is temporarily set to every 10 seconds
            # trigger=CronTrigger(second="*/30"),

            # We send emails to subscribers on Monday at 8 am
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),

            # Same as interval, but the trigger's task is thus more clear to django
            id="news_sender",  # unique ID
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added work 'news_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="19", minute="00"
            ),
            # Every week old tasks that either could not be completed will be deleted
            # or there is no need to execute it anymore.

            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("The task book is running")
            print('The task book is running')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Problem book stopped")
            scheduler.shutdown()
            print('Problem book stopped')
            logger.info("The task manager stopped successfully!")
