import json
import math
import argparse
from datetime import datetime, timedelta

class ScheduleEntry():
    # Represents a single entry in the schedule

    def __init__(self, user, start, end):
        self.user = user
        self.start = start
        self.end = end
    
    def to_json(self):
        return {
            "user": self.user,
            "start_at": self.start.isoformat().replace("+00:00", "Z"),
            "end_at": self.end.isoformat().replace("+00:00", "Z"),
        }

def parse_time(time):
    return datetime.fromisoformat(time.replace("Z", "+00:00"))

def load_files(schedule_file, overrides_file):
    try:
        with open(schedule_file, 'r') as sf:
            schedule = json.load(sf)
    except json.JSONDecodeError:
        return [], []
    try:
        with open(overrides_file, 'r') as of:
            overrides = json.load(of)
    except json.JSONDecodeError:
        overrides = []

    # Assuming the overrides aren't sorted
    overrides = sorted(overrides, key=lambda x: parse_time(x["start_at"])) if overrides else []
    return schedule, overrides

def create_schedule(schedule, overrides, from_time, until):
    handover_start = parse_time(schedule["handover_start_at"])
    handover_interval = timedelta(days = schedule["handover_interval_days"])
    users = schedule["users"]

    if handover_start < from_time:
        start = from_time
        end = ((from_time - handover_start) // handover_interval + 1) * handover_interval + handover_start # End time of an interval, adjusted to be at the end of the interval which contains the from_time
        user = ((from_time - handover_start) // handover_interval) % len(users) # Index of the expected user to run in the interval containing the from_time
    else:
        start = handover_start
        end = start + handover_interval
        user = 0

    # Index of the override, adjusted to contain the from_time
    override = 0
    while override < len(overrides) and parse_time(overrides[override]["end_at"]) <= from_time:
        override += 1
    
    res = []
    while override < len(overrides) and start <= until:
        override_start = max(parse_time(overrides[override]["start_at"]), from_time) 
        override_end = parse_time(overrides[override]["end_at"])

        if start < override_start < end: # Schedule the user until the start of the next override
            res.append(ScheduleEntry(users[user], start, override_start))
            start = override_start
        elif start == override_start: # Schedule the override
            res.append(ScheduleEntry(overrides[override]["user"], override_start, override_end))
            start = override_end
            override += 1
        else: # No overrides in this interval
            res.append(ScheduleEntry(users[user], start, end))
            start = end
        while end <= start: # Use a while loop in case an override spans multiple intervals
            end += handover_interval
            user = (user + 1) % len(users)
    
    # After exhausting the overrides, fill in the rest of the schedule
    while until >= start:
        res.append(ScheduleEntry(users[user], start, end))
        start = end
        end += handover_interval
        user = (user + 1) % len(users)
    
    # Truncate to 'until'. It's possible that the start time of the last scheduled entry is the 'until' time so return everything except the last entry 
    if res:
        res[-1].end = min(res[-1].end, until)
        if res[-1].start >= res[-1].end:
            res.pop()  
    return res


def main():
    parser = argparse.ArgumentParser(description="Render on-call schedule with overrides.")
    
    parser.add_argument(
        "--schedule", 
        required=True, 
        help="Path to the schedule JSON file"
    )
    parser.add_argument(
        "--overrides", 
        required=True, 
        help="Path to the overrides JSON file"
    )
    parser.add_argument(
        "--from", 
        required=True, 
        dest="from_time",
        help="Start time in ISO 8601 format"
    )
    parser.add_argument(
        "--until", 
        required=True, 
        help="End time in ISO 8601 format"
    )
    args = parser.parse_args()
    from_time = parse_time(args.from_time)
    until_time = parse_time(args.until)
    schedule, overrides = load_files(args.schedule, args.overrides)
    if not schedule:
        print(json.dumps([]))
        return
    res = create_schedule(schedule, overrides, from_time, until_time)
    print(json.dumps([entry.to_json() for entry in res], indent=2))

if __name__ == "__main__":
    main()