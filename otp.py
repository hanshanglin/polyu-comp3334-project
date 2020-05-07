import time
import random
import math
import os

class OTP:
    TickIntervalSeconds=30
    PasscodeLength=6
    _rng=random.SystemRandom()

    def __init__(self, tick_interval, passcode_len):
        self.TickIntervalSeconds=int(abs(tick_interval))
        self.PasscodeLength=int(abs(passcode_len))

    def generate_seed(self):
        seed=0
        for n in range(1,self.PasscodeLength+1):
            seed=seed*10+self._rng.randint(0,10)
        return seed

    def _get_current_interval(self):
        sec=int(math.floor(time.time()))
        return sec//self.TickIntervalSeconds

    def _get_current_passcode(self, seed):
        tick=self._get_current_interval()
        p=tick*tick*seed % (10**self.PasscodeLength)
        return p

    def check(self, seed, passcode):
        return self._get_current_passcode()==passcode

    def get_OTP_client_android(self, seed, designated_name=None):
        if designated_name==None:
            designated_name="%08x"%random.getrandbits(32)+".apk"
        os.system("./modapk/modapk.sh OTP_PoC.apk 1.apk -w assets/OTP_seed.txt "+str(seed))
        os.replace("/modapk/1.apk", "designated_name")
        return designated_name

    def get_OTP_client_win(self, seed, designated_name=None):
        if designated_name==None:
            designated_name="%08x"%random.getrandbits(32)+".py"
        f=open(designated_name, "w")
        f.write("TickIntervalSeconds="+str(self.TickIntervalSeconds))
        f.write("\nPasscodeLength="+str(self.PasscodeLength))
        f.write("\nseed="+str(seed))
        f.write("\n")
        template=open("otp_win_template.py", "r")
        f.write(template.read())
        return designated_name

OTPPreset=OTP(30,6)


if __name__=="__main__":
    _otpobject=OTP(30,6)
    _sd=_otpobject.generate_seed()
    print("time: ", time.time())
    print(_otpobject._get_current_interval())
    print(_otpobject._get_current_passcode(_sd))
    print(_otpobject.get_OTP_client_win(_sd))
