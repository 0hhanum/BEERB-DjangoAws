# 달력 구현하기.

import calendar


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for date in week:
                days.append(date[0])
        return days
