import json
from datetime import datetime

class Schedule():
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

def parse_time(time):
    return datetime.fromisoformat(time.replace("Z", "+00:00"))

def load_files(schedule_file, override_file):
    with open(schedule_file, 'r') as sf:
        schedule = json.load(sf)
    with open(override_file, 'r') as of:
        overrides = json.load(of)

    overrides = sorted(overrides, key=lambda x: parse_time(x["start_at"]))
    return schedule, overrides

def main():
    schedule, overrides = load_files("./schedule.json", "./overrides.json")
    print(schedule)
    print(overrides)

main()