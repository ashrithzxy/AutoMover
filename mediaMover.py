from connection import Connection
from backup import Backup

device = Connection()
adbConnectionStatus = device.establishAdbConnection()
print("Adb Connection Status is: ",adbConnectionStatus)
if adbConnectionStatus is False:
    print('unable to establish adb connection. Check logs.')
else:
    pass
    # # start backup process.
    # mediaBackup = Backup()
    # mediaBackup.createBackup()
