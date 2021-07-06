from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "This command create superuser"

    def handle(self, *args, **options):
        User.objects
        self.stdout.write(self.style.SUCCESS(f"{number} users CREATED"))
