from timer import Timer
from collections import OrderedDict
from tabulate import tabulate

class Timers:

    STAT_LABELS = [  
        'name',
        'mean',
        'median',
        'min',
        'max',
        '5% low',
        '5% high',
    ]

    def __init__(self):
        self.timers = OrderedDict()

    def start(self,label):
        if label not in self.timers:
            self.timers[label] = Timer(label)

        self.timers[label].start()

    def stop(self,label):
        if label not in self.timers:
            raise RuntimeError(
                f'timer with label {label} does not exist'
            )

        self.timers[label].stop()
    
    def printStats(self):
        # collect data
        data = []
        for label,timer in self.timers.items():
            timerData = [label] + list(timer.getStats())
            data.append(timerData)

        # !! praise the tabulate library author !!
        print(tabulate(data,headers=Timers.STAT_LABELS,tablefmt='github'))
        