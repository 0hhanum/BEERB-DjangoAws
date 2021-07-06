from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command create superuser"

    def handle(self, *args, **options):
        try:
            User.objects.get(username="ebadmin")
            User.objects("ebadmin", "rntls123@naver.com", "123")
            self.stdout.write(self.style.SUCCESS("Supersuer Created"))
        except User.DoesNotExist:
            pass
