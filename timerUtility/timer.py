from time import time_ns
from statistics import pstdev


class Timer:

    TABLE_FORMAT = 1
    NS_TO_S = lambda ns: ns / (10 ** 9)
    S_TO_NS = lambda s: s * (10 ** 9)

    def __init__(self, name: str, raiseErrors: bool = False):
        self.name: str = name
        self.raiseErrors: bool = raiseErrors
        self.startTime: float = -1.0
        self.history: list[float] = []
    
    def print(self, s):
        print(f'[Timer] {s}')

    def start(self):
        if self.startTime != -1.0:
            errstr = f'start called twice in a row for timer: {self.name}'
            if self.raiseErrors:
                raise RuntimeError(errstr)
            else:
                self.print(errstr)
        
        self.startTime = Timer.NS_TO_S(time_ns())

    def stop(self):
        if self.startTime == -1.0:
            errstr = f'end called before start for timer: {self.name}'
            if self.raiseErrors:
                raise RuntimeError(errstr)
            else:
                self.print(errstr)

        runtime = Timer.NS_TO_S(time_ns()) - self.startTime
        self.history.append(runtime)
        self.startTime = -1

    def getStats(self):
        sortedHistory = sorted(self.history)

        mean = sum(sortedHistory) / len(sortedHistory)
        median = sortedHistory[len(sortedHistory) // 2]
        stddev = pstdev(sortedHistory)
        mini = min(sortedHistory)
        maxi = max(sortedHistory)
        fivePercLow = sortedHistory[len(sortedHistory) // 20]
        fivePercHigh = sortedHistory[(len(sortedHistory) // 20) * 19]

        return (mean,median,stddev,mini,maxi,fivePercLow,fivePercHigh)
        