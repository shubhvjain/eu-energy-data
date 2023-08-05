from datetime import datetime, timedelta
import pandas as pd


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


def convertTo60MinInterval(rawData, start, end):
    duration = rawData["duration"]
    if duration == 60:
        """ If the duration is already 60, return data """
        return rawData["data"]
    elif duration < 60:
        """
        First, we determine the number of rows needed to combine in order to obtain data in a 60-minute format. 
        It is important to note that the rows are combined by taking the average of the row data, rather than the sum.
        """
        # determing how many rows need to be combined to get data in 60 min format. The rows are com
        groupingFactor = int(60/duration)
        oldData = rawData["data"]
        dataColToRemove = ['startTime', 'endTime']
        oldData = oldData.drop(dataColToRemove, axis=1)
        oldData['group_id'] = oldData.index // groupingFactor
        newGroupedData = oldData.groupby('group_id').mean()
        timeUTCInterval = countIntervals(start, end, 60)
        newGroupedData["startTime"] = timeUTCInterval["startBin"]
        newGroupedData["endTime"] = timeUTCInterval["endBin"]
        return newGroupedData
