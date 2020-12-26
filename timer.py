from time import time_ns

class Timer:

    TABLE_FORMAT = 1
    NS_TO_S = lambda ns: ns / (10 ** 9)
    S_TO_NS = lambda s: s * (10 ** 9)

    def __init__(self,name):
        self.name = name
        self.startTime = None
        self.history = []

    def start(self):
        if self.startTime is not None:
            raise RuntimeError(
                f'start called twice in a row for timer: {self.name}'
            )
        
        self.startTime = Timer.NS_TO_S(time_ns())

    def stop(self):
        if self.startTime is None:
            raise RuntimeError(
                f'end called before start for timer: {self.name}'
            )

        runtime = Timer.NS_TO_S(time_ns()) - self.startTime
        self.history.append(runtime)
        self.startTime = None

    def getStats(self):
        sortedHistory = sorted(self.history)

        mean = sum(sortedHistory) / len(sortedHistory)
        median = sortedHistory[len(sortedHistory) // 2]
        mini = min(sortedHistory)
        maxi = max(sortedHistory)
        fivePercLow = sortedHistory[len(sortedHistory) // 20]
        fivePercHigh = sortedHistory[(len(sortedHistory) // 20) * 19]

        return (mean,median,mini,maxi,fivePercLow,fivePercHigh)