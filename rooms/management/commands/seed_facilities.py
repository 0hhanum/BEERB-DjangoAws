from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = "This command create facilities"

    """
    def add_arguments(self, parser):

        parser.add_argument(
            "--times",
            help="How many times run?",
        )
    """

    def handle(self, *args, **options):

        facilities = ["건물 내 무료 주차", "헬스장", "자쿠지", "수영장"]

        for facility in facilities:
            if not Facility.objects.filter(name=facility):
                Facility.objects.create(name=facility)

        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} created!"))

        # times = options.get("times")

        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.SUCCESS("GOOD!"))
