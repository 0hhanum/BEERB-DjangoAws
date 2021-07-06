from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command create superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects("ebadmin", "rntls123@naver.com", "123")
            self.stdout.write(self.style.SUCCESS("Supersuer Created"))
