## Insanely Simple Loop-Friendly Profiling Utility

### Interface

timers (class) - manager for multiple timer classes

```python
timers = Timers()
timers.start(TIMER_LABEL)
timers.end(TIMER_LABEL)
timers.printStats()
```
