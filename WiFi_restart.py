import subprocess
import time

count = 0
no_wifi = True

while no_wifi:
    ping_ret = subprocess.call(['ping -c 2 -w 1 -q 192.168.10.1 |grep "1 received" > /dev/null 2> /dev/null'], shell=True)
    if ping_ret:
        # we lost the WLAN connection.
        count = count + 1

        # try to recover the connection by resetting the LAN
        print "resetting WiFi ", count
        subprocess.call(['logger "WLAN is down, Pi is resetting WLAN connection"'], shell=True)
        WLAN_check_flg = True # try to recover
        subprocess.call(['sudo /sbin/ifdown wlan0 && sleep 10 && sudo /sbin/ifup --force wlan0'], shell=True)
    else:
        no_wifi = False
        
    if count > 5:
        print "resetting Pi"
        # we have a serious problem and need to reboot the Pi to recover the WLAN connection
        subprocess.call(['logger "WLAN Down, Pi is forcing a reboot"'], shell=True)
        subprocess.call(['sudo reboot'], shell=True)

    time.sleep(5)
