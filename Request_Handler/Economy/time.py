from datetime import datetime, timedelta
from django.http import HttpResponse

price = 60


def checkTime(start, end):
    if end > start:
        print(start)
        print(end)
        nextTime = datetime.now() + timedelta(minutes=15)
        nextAddedTIme = datetime.now() + timedelta(minutes=25)
        if (start >= nextTime) & (start <= nextAddedTIme):
            return True
        else:
            print('b')
            return False

    else:
        return False


def getAmount(start, end):
    diff = end - start
    diff = str(diff).split(':', 3)
    total = 0
    for i in range(0, 2):
        if i == 0:
            total += float(diff[i]) * price
        if i == 1:
            total += ((float(diff[i]) / 60)) * price
    return total
