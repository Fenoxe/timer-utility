from collections import OrderedDict

from tabulate import tabulate

from .timer import Timer


class Timers:

    STAT_LABELS = [
        'name',
        'mean',
        'median',
        'stddev',
        'min',
        'max',
        '5% low',
        '5% high',
    ]

    def __init__(self, raiseErrors: bool = False, profilerLoop: list[str] = []):
        self.timers = OrderedDict()
        self.raiseErrors: bool = raiseErrors

        if len(profilerLoop) > 0:
            self.profilerLoop = profilerLoop
            self.currProfileI = -1
            for name in self.profilerLoop:
                self.create(name)

    def print(self, s):
        print(f'[Timers] {s}')

    def create(self, name):
        if name in self.timers:
            errstr = f'timer with name {name} already exists'
            if self.raiseErrors:
                raise RuntimeError(errstr)
            else:
                self.print(errstr)
        
        self.timers[name] = Timer(name, raiseErrors=self.raiseErrors)

    def start(self, name):
        if name not in self.timers:
            self.create(name)

        self.timers[name].start()

    def stop(self, name):
        if name not in self.timers:
            errstr = f'timer with name {name} does not exist'
            if self.raiseErrors:
                raise RuntimeError(errstr)
            else:
                self.print(errstr)

        self.timers[name].stop()

    def profilerBreak(self):
        if len(self.profilerLoop) == 0:
            errstr = f'attempted to use profilerBreak without initializing profiler loop'
            if self.raiseErrors:
                raise RuntimeError(errstr)
            else:
                self.print(errstr)
        
        if self.currProfileI >= 0:
            self.stop(self.profilerLoop[self.currProfileI])
        self.currProfileI = (self.currProfileI + 1) % len(self.profilerLoop)
        self.start(self.profilerLoop[self.currProfileI])
        
    
    def printStats(self):
        # collect data
        data = []
        for label,timer in self.timers.items():
            timerData = [label] + list(timer.getStats())
            data.append(timerData)

        # !! praise the tabulate library author !!
        print(tabulate(data,headers=Timers.STAT_LABELS,tablefmt='github'))
        
    def getTimes(self):
        return { timerName: timer.history for timerName,timer in self.timers.items() }