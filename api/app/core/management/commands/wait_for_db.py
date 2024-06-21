import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OperationalError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                self.stdout.write(self.style.SUCCESS('Database available!'))
            except (OperationalError, Psycopg2OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
