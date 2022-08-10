from app import *

class Frequency:
    DAILY = 0
    WEEKLY = 1

def get_upcoming_tasks(assignment):
    if assignment.frequency == Frequency.DAILY:
        # TODO: add metadata option to exclude weekends
        today = date.today()
        tomorrow = date.today() + timedelta(days=1)
        return [today, tomorrow]
    elif assignment.frequency == Frequency.WEEKLY:
        U = (assignment.frequency_metadata >> 6) & 1
        M = (assignment.frequency_metadata >> 5) & 1
        T = (assignment.frequency_metadata >> 4) & 1
        W = (assignment.frequency_metadata >> 3) & 1
        H = (assignment.frequency_metadata >> 2) & 1
        F = (assignment.frequency_metadata >> 1) & 1
        S = (assignment.frequency_metadata >> 0) & 1

        # aligned with weekday() (0 = M, 1 = T, etc.)
        occurs = [M, T, W, H, F, S, U]

        this_week = []
        next_week = []
        day = date.today()

        # aggregate all remaining days this week
        while True:
            if occurs[day.weekday()]:
                this_week.append(day)
            day += timedelta(days=1)
            if day.weekday() == 6:
                break

        # aggregate all days next week
        while True:
            if occurs[day.weekday()]:
                next_week.append(day)
            day += timedelta(days=1)
            if day.weekday() == 6:
                break

        return [this_week, next_week]
