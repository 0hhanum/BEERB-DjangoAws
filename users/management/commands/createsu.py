import os
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command create superuser"

    def handle(self, *args, **options):
        admin_id = os.environ.get("admin")
        admin_password = os.environ.get("ad_password")

        admin = User.objects.get_or_none(username=admin_id)
        if not admin:
            User.objects.create_superuser(
                admin_id,
                "rntls123@naver.com",
                admin_password,
            )
            self.stdout.write(self.style.SUCCESS("Supersuer Created"))
