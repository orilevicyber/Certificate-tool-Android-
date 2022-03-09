from ppadb.client import Client as AdbClient
import pyfiglet
import os
import time
import fileinput
import re

print(pyfiglet.figlet_format("Certificate tool", font="cybermedium"))

try:
 der = (input('Insert Path Der: '))
 os.system("openssl x509 -inform der -in " + der + " -out mobile.pem")
 os.system("openssl x509 -inform PEM -subject_hash_old -in mobile.pem > mobile.txt")
 os.system("adb devices > devices.txt")
 fd = open("mobile.txt", "r")
 lines = fd.readlines()[0:1]
 for line in lines:
    nameHash = line.rstrip()
    fd.close()
    crt = nameHash + ".0"
    os.system("move mobile.pem " + crt)
    os.system("adb push " + crt + " /sdcard/")

    fdd = open("devices.txt", "r")
    lines = fdd.readlines()[1:2]
    for line in lines:
     data = line.rstrip()

    for devices in fileinput.input("devices.txt"):
     ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', devices)
    if ip:
       for i in ip:
        client = AdbClient(host="127.0.0.1", port=5037)
        client.remote_connect(i, 5555)
        device = client.device(str(i + ":" + "5555"))
        time.sleep(2)
        response1 = device.remount()
        time.sleep(2)
        response2 = device.shell('mv /sdcard/9a5ba575.0 /system/etc/security/cacerts/')
        time.sleep(2)
        response3 = device.shell('chmod 644 /system/etc/security/cacerts/9a5ba575.0')
        response4 = device.reboot()
        print("Success")

except:
  print("Connection Error")
