import os

def genapk(dest_file, seed, tempdir="tmp_apk\\",):
    cwd=os.getcwd()
    wd=os.getcwd()+"\\"+tempdir
    if not os.path.exists(wd):
        os.mkdir(wd)
    os.chdir(wd)
    os.system("jar -xf "+cwd+"\\modapk\\OTP_PoC.apk")

    f=open(wd+"\\assets\\OTP_seed.txt", "w")
    f.write(str(seed))
    f.close()

    os.system("jar -cfM "+wd+"\\out.apk *")
    os.system('jarsigner -keystore '+cwd+'\\modapk\\android.keystore -storepass "android" -keypass "android" -signedjar '+wd+'\\signed.apk '+wd+'\\out.apk "androidkey"')
    os.rename("signed.apk", cwd+"\\"+dest_file)
    os.chdir(cwd)
    os.system("rmdir "+wd+" /s /q")

