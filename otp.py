import time
import random
import math
import os
import modapk_win

__PLATFORM__="WINDOWS"

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
        _passcode=int(passcode)
        if isinstance(passcode, str):
            _passcode=0
            a=1
            for i in range(self.PasscodeLength):
                _passcode=_passcode+a*int(passcode[-1-i])
                a*=10
        return self._get_current_passcode(seed)==_passcode

    def get_OTP_client_android(self, seed, designated_name=None):
        if designated_name==None:
            designated_name="%08x"%random.getrandbits(32)+".apk"
        if __PLATFORM__=="WINDOWS":
            modapk_win.genapk(designated_name,seed)
            return designated_name
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
    print(_otpobject.check(_sd,str(_otpobject._get_current_passcode(_sd)).zfill(6)))
