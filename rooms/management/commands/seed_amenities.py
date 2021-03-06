from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command create Amenities"

    def add_arguments(self, parser):

        parser.add_argument(
            "--times",
            help="How many times run?",
        )

    def handle(self, *args, **options):

        amenities = [
            "주방",
            "샴푸",
            "난방",
            "에어컨",
            "세탁기",
            "건조기",
            "무선 인터넷",
            "아침 식사",
            "실내 벽난로",
            "옷걸이",
            "다리미",
            "헤어드라이어",
            "업무",
            "전용 공간",
            "TV",
            "아기 침대",
            "유아용 식탁의자",
            "셀프",
            "체크인",
            "화재경보기",
            "일산화탄소",
            "경보기",
            "욕실",
            "단독 사용",
            "피아노",
            "해변에 인접",
            "수변에 인접",
            "스키를 탄 채로 출입 가능",
        ]

        for amenity in amenities:
            if not Amenity.objects.filter(name=amenity):
                Amenity.objects.create(name=amenity)

        self.stdout.write(self.style.SUCCESS("Amenities created!"))

        # times = options.get("times")

        # for t in range(0, int(times)):
        #     self.stdout.write(self.style.SUCCESS("GOOD!"))
