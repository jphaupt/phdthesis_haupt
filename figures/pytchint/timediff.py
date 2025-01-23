import sys
from datetime import datetime

def time_difference(time1: str, time2: str) -> int:
    """
    Calculate the difference between two times in seconds.
    :param time1: First time in format "hh:mm:ss"
    :param time2: Second time in format "hh:mm:ss"
    :return: Absolute difference in seconds
    """
    time_format = "%H:%M:%S"
    t1 = datetime.strptime(time1, time_format)
    t2 = datetime.strptime(time2, time_format)
    return abs(int((t2 - t1).total_seconds()))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <time1> <time2>")
        sys.exit(1)

    time1 = sys.argv[1]
    time2 = sys.argv[2]
    print("Time difference in seconds:", time_difference(time1, time2))
