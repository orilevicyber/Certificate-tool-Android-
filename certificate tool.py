import pyfiglet
import os
from ppadb.client import Client as AdbClient


print(pyfiglet.figlet_format("Certificate tool", font ="cybermedium"))


try:
 os.system("adb devices > devices.txt")

 print("Insert path Der")
 der = input()
 os.system("openssl x509 -inform der -in "+der+" -out mobile.pem")
 os.system("openssl x509 -inform PEM -subject_hash_old -in mobile.pem > mobile.txt")

 fd = open("mobile.txt","r")
 lines = fd.readlines()[0:1]
 for line in lines:
  nameHash = line.rstrip()
 fd.close()
 crt = nameHash+".0"
 os.system("move mobile.pem "+crt)
 os.system("adb push " +crt+ " /sdcard/")

 fdd = open("devices.txt","r")
 lines = fdd.readlines()[1:2]
 for line in lines:
  data = line.rstrip()
 ipPort = data[0:19]
 ip = data[0:14]
 port = data[15:19]
 client = AdbClient(host="127.0.0.1", port=5037)
 client.remote_connect(ip, 5555)
 device = client.device(str(ipPort))

 response1 = device.remount()
 response2 = device.shell('mv /sdcard/9a5ba575.0 /system/etc/security/cacerts/')
 response3 = device.remount()
 response4 = device.remount()
 response5 = device.shell('chmod 644 /system/etc/security/cacerts/9a5ba575.0')
 response6 = device.shell('chmod 644 /system/etc/security/cacerts/9a5ba575.0')
 response7 = device.reboot()


except:
  print("Connection Error")
