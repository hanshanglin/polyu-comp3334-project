import os
import shutil
import schedule
import time

__TARGET_FILES__=["profiles.json"]
__TARGET_DIRS__=["storage/"]

def backup():
    if not os.path.exists("bak"):
        os.mkdir("bak")
    if os.path.exists("bak_old"):
        shutil.rmtree("bak_old")

    shutil.move("bak", "bak_old", copy_function = shutil.copytree)
    os.mkdir("bak")
    
    for item in __TARGET_FILES__:
        shutil.copyfile(item, "bak/"+item)
    for item in __TARGET_DIRS__:
        shutil.copytree(item, "bak/"+item)

    print("Backup completed")




backup()
schedule.every().day.at("03:00").do(backup)
while True: 
    schedule.run_pending() 
    time.sleep(1) 
