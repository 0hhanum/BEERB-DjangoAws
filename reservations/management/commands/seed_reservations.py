import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

NAME = "reservations"


class Command(BaseCommand):

    help = f"This command create {NAME}"

    def add_arguments(self, parser):

        parser.add_argument(
            "--total",
            type=int,
            default=1,
            help=f"How many {NAME} you want to create?",
        )

    def handle(self, *args, **options):
        total = options.get("total")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reservation_models.Reservation,
            total,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now()
                + timedelta(days=random.randint(1, 60)),
                "check_out": lambda x: 0,
            },
        )

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{total} {NAME} created!"))
