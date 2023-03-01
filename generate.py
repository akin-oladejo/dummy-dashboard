from faker import Faker
from dataclasses import dataclass
import random

# import pandas as pd
from pprint import pprint

fake = Faker()


@dataclass
class Calls:
    log = []

    def one_call(self):
        day = int(fake.day_of_month())
        start_time = random.choice(["9", "10", "11", "12", "1", "2", "3", "4", "5"])
        call_type = random.choice(["inbound", "outbound"])
        status = (
            "successful"
            if random.choice([0, 1])
            else random.choice(["abandoned", "missed", "voicemail"])
        )
        duration = random.randint(3, 240) if status != "missed" else 0
        dest = random.choice(["Nigeria", "France", "Algeria", "Sweden"])
        down_time = random.uniform(0, 2)

        return [day, start_time, duration, call_type, status, dest, down_time]

    def many_calls(self, n):
        for i in range(n):
            self.log.append(self.one_call())

        return {
            "columns": [
                "day",
                "start_time",
                "duration",
                "call_type",
                "status",
                "dest",
                "down_time",
            ],
            "data": self.log,
        }
