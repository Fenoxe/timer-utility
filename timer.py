from time import time_ns

from math import stddev

class Timer:

    TABLE_FORMAT = 1
    NS_TO_S = lambda ns: ns / (10 ** 9)
    S_TO_NS = lambda s: s * (10 ** 9)

    def __init__(self, name: str):
        self.name: str = name
        self.startTime: float = -1.0
        self.history: list[float] = []

    def start(self):
        if self.startTime != -1.0:
            raise RuntimeError(
                f'start called twice in a row for timer: {self.name}'
            )
        
        self.startTime = Timer.NS_TO_S(time_ns())

    def stop(self):
        if self.startTime == -1.0:
            raise RuntimeError(
                f'end called before start for timer: {self.name}'
            )

        runtime = Timer.NS_TO_S(time_ns()) - self.startTime
        self.history.append(runtime)
        self.startTime = -1

    def getStats(self):
        sortedHistory = sorted(self.history)

        mean = sum(sortedHistory) / len(sortedHistory)
        median = sortedHistory[len(sortedHistory) // 2]
        std = stddev(sortedHistory)
        mini = min(sortedHistory)
        maxi = max(sortedHistory)
        fivePercLow = sortedHistory[len(sortedHistory) // 20]
        fivePercHigh = sortedHistory[(len(sortedHistory) // 20) * 19]

        return (mean,median,std,mini,maxi,fivePercLow,fivePercHigh)
        