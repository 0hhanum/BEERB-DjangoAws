# 달력 구현하기.
from django.utils import timezone
import calendar


class Day:
    def __init__(self, number, past, month, year):

        self.number = number
        self.past = past
        self.month = month
        self.year = year

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        now = timezone.now()
        today = now.day
        for week in weeks:
            for day, _ in week:
                new_day = Day(day, day < today, month=self.month, year=self.year)
                days.append(new_day)
        return days
