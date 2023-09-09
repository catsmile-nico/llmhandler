from datetime import datetime
import pytz

from .base import create_tool

def init():
    return create_tool(
        "timezone_difference", 
        "Calculates the time difference for 2 given location", 
        location_1={"type": "string", "description": "Timezone to be compared e.g. Asia/Tokyo"}, 
        location_2={"type": "string", "description": "Timezone to be compared e.g. Asia/Tokyo"}
    )

def run(location_1, location_2):
    time1 = datetime.now(pytz.timezone(location_1))
    time2 = datetime.now(pytz.timezone(location_2))

    # Calculate the difference in hours and minutes
    time_difference_in_minutes = ((time2.hour * 60 + time2.minute) - (time1.hour * 60 + time1.minute))

    hours, minutes = divmod(abs(time_difference_in_minutes), 60)

    # Determine if the time is ahead or behind local time
    difference = "behind" if time_difference_in_minutes < 0 else "after"
    time_difference_str = f'{hours} hours, {minutes} minutes {difference}'

    return time_difference_str

