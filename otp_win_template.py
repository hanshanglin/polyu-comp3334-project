import time
import math

def _get_current_interval():
    sec=int(math.floor(time.time()))
    return sec//TickIntervalSeconds

def _get_current_passcode(seed):
    tick=_get_current_interval()
    p=tick*tick*seed % (10**PasscodeLength)
    return p

last_update_tick=0
fmt="%0"+str(PasscodeLength)+"d"
while True:
    if last_update_tick!=_get_current_interval():
        print(fmt%_get_current_passcode(seed))
        last_update_tick=_get_current_interval()
