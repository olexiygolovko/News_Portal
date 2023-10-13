from django.core.management.base import BaseCommand, CommandError
from news.models import Post

class Command(BaseCommand):
    help = 'Remove news from category'  # shows a hint when typing "python manage.py <your command> --help"
    requires_migrations_checks = True  # whether to remind about migrations. If you do, there will be a reminder that all migrations have not been completed (if any)

    def handle(self, *args, **options):
        # here you can write any code that will be executed when your command is called
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete news? yes/no')  # we ask the user if he really wants to delete all news
        answer = input()  # read the confirmation

        if answer == 'yes':  # If confirmed, we will indeed remove all products.
            Post.objects.get(pk=1).categoryType.delete(pk=1)
            self.stdout.write(self.style.SUCCESS('Succesfully wiped news!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # in case of incorrect confirmation, we say that access is denied