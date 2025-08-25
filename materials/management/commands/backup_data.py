from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'Backup all data to fixtures'

    def handle(self, *args, **options):
        management.call_command('dumpdata', 'materials', 'users',
                                indent=4,
                                output='backup/data.json')
        self.stdout.write(self.style.SUCCESS('Successfully backed up data'))
