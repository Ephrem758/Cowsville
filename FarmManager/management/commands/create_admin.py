"""
Management command to create admin users for the Farm Manager application
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Create an admin user for accessing GET endpoints'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='Username for the admin user'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the admin user (if not provided, will prompt)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@farmmanager.local',
            help='Email for the admin user'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Prompt for password if not provided
        if not password:
            password = self.style.SUCCESS('Enter password: ')
            password = input(password)

        try:
            # Create the admin user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Make the user a staff member (admin)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user: {username}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'This user can now access all GET endpoints using Basic Auth or Django sessions.'
                )
            )

        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(
                    f'User {username} already exists!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error creating user: {str(e)}'
                )
            ) 