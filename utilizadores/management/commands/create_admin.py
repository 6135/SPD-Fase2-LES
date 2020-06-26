import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from utilizadores.models import Administrador


class Command(BaseCommand):
    help = 'Cria o primeiro administrador. Exemplo: manage.py create_admin password123'

    def add_arguments(self, parser):
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        if Administrador.objects.all().count() > 0:
            raise CommandError('Este comando só pode ser usado quando não existe nenhum administrador')

        admin = Administrador.objects.create(username="admin", first_name="admin", last_name="admin", password="", valido="True")
        admin.set_password(options['password'])
        admin.save()

        self.stdout.write(self.style.SUCCESS('Administrador criado com sucesso! username: "admin" '))
