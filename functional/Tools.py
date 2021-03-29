from datetime import datetime
from typing import List


def CurierWeight(typecur):
    if typecur == 'foot':
        return 10
    if typecur == 'bike':
        return 15
    if typecur == 'car':
        return 50



def GetStriptime(time: str):
    return datetime.strptime(time, '%H:%M')


def IntersectionTimes(time1: List[str], time2: List[str]) -> bool:
    for t1 in time1:
        for t2 in time2:
            start_time1 = t1.split('-')[0]
            finish_time1 = t1.split('-')[1]
            start_time2 = t2.split('-')[0]
            finish_time2 = t2.split('-')[1]
            arr_time = [start_time1, finish_time1, start_time2, finish_time2]
            arr_time = list(map(GetStriptime, arr_time))
            if arr_time[0] < arr_time[3] and arr_time[1] > arr_time[2]:
                return True

    return False


def NowRFC_3339() -> str:
    d = datetime.utcnow()
    return d.isoformat("T")[0:22] + "Z"


def DeltaSecondRFC_3339(time_start: str, time_end: str):
    time_start = datetime.strptime(time_start[0:22], '%Y-%m-%dT%H:%M:%S.%f')
    time_end = datetime.strptime(time_end[0:22], '%Y-%m-%dT%H:%M:%S.%f')
    return int((time_end - time_start).total_seconds())

#
# str1 = "2021-03-28T23:21:50.87Z"
# str2 = "2021-03-28T23:22:00.87Z"
# print(DeltaSecondRFC_3339(str1, str2))


def Selary(delivery, selary_str) -> int:
    res = 0
    for i in range(0, delivery):
        if selary_str[i] == 'F':
            res += 2 * 500
        elif selary_str[i] == 'B':
            res += 5 * 500
        elif selary_str[i] == 'C':
            res += 9 * 500

    return res
#
#
# print(Selary(4, 'FFFBB'))
