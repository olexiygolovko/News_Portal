from django.core.management.base import BaseCommand, CommandError
from news.models import Post

class Command(BaseCommand):
    help = 'Удалить новости из категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можно писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete news? yes/no')  # спрашиваем пользователя действительно ли он хочет удалить все новости
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            Post.objects.get(pk=1).categoryType.delete(pk=1)
            self.stdout.write(self.style.SUCCESS('Succesfully wiped news!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим что в доступе отказано