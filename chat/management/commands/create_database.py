from django.core.management.base import BaseCommand
from django.core.management import call_command
import mysql.connector
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates the MySQL database if it does not exist and runs migrations'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        config = {
            'user': db_settings['USER'],
            'password': db_settings['PASSWORD'],
            'host': db_settings['HOST'],
            'port': db_settings['PORT'],
        }

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            try:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_settings['NAME']}")
                self.stdout.write(self.style.SUCCESS(f'Successfully created database {db_settings["NAME"]}'))
                
                # Run migrations to create tables
                self.stdout.write('Running migrations to create tables...')
                call_command('migrate')
                self.stdout.write(self.style.SUCCESS('Successfully created all database tables'))
                
            except mysql.connector.Error as err:
                self.stdout.write(self.style.ERROR(f'Failed to create database: {err}'))
            finally:
                cursor.close()
                conn.close()
        except mysql.connector.Error as err:
            self.stdout.write(self.style.ERROR(f'Failed to connect to MySQL: {err}'))