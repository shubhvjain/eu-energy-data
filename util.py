from datetime import datetime, timedelta

def countIntervals(startDate, endDate, intervalMinutes):
    startDatetime = datetime.strptime(startDate, "%Y%m%d%H%M")
    endDatetime = datetime.strptime(endDate, "%Y%m%d%H%M")
    interval = timedelta(minutes=intervalMinutes)
    startBin = []
    endBin = []
    count = 0
    while startDatetime < endDatetime:
        a = startDatetime.strftime("%Y%m%d%H%M")
        count += 1
        startDatetime += interval
        b = startDatetime.strftime("%Y%m%d%H%M")
        startBin.append(a)
        endBin.append(b)
    return {"count":count,"startBin":startBin,"endBin":endBin}

