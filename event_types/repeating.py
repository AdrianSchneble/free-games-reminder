import json

WEEKDAY_TO_INT_MAPPING = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 0,
}


def map_weekday_name_to_int(days: list[str]) -> list[int]:
    return [WEEKDAY_TO_INT_MAPPING[day] for day in days]


class RepeatingEvent:
    # required
    message: str
    timezone: str
    hour: int

    # optional
    minute: int
    second: int
    days: list[int]

    def __init__(
        self,
        message: str,
        timezone: str,
        hour: int,
        minute: int = 0,
        second: int = 0,
        days: list[str] | None = None,
    ):
        self.message = message
        self.timezone = timezone
        self.hour = hour
        self.minute = minute
        self.second = second
        self.days = map_weekday_name_to_int(days) if days else list(range(7))

    def __str__(self) -> str:
        print(type(self.timezone))
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
