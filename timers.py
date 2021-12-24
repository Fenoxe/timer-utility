from timer import Timer
from collections import OrderedDict
from tabulate import tabulate

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

    def __init__(self, raiseErrors: bool = False):
        self.timers = OrderedDict()
        self.raiseErrors: bool = raiseErrors

    def print(self, s):
        print(f'[Timers] {s}')

    def start(self,label):
        if label not in self.timers:
            self.timers[label] = Timer(label, raiseErrors=self.raiseErrors)

        self.timers[label].start()

    def stop(self,label):
        if label not in self.timers:
            errstr = f'timer with label {label} does not exist'
            if self.raiseErrors:
                raise RuntimeError(errstr)
            else:
                self.print(errstr)

        self.timers[label].stop()
    
    def printStats(self):
        # collect data
        data = []
        for label,timer in self.timers.items():
            timerData = [label] + list(timer.getStats())
            data.append(timerData)

        # !! praise the tabulate library author !!
        print(tabulate(data,headers=Timers.STAT_LABELS,tablefmt='github'))
        
        