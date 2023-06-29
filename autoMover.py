from connection import Connection
from backup import Backup
from pprint import pprint

device = Connection()
adbConnectionStatus = device.establishAdbConnection()
print("Adb Connection Status is: ",adbConnectionStatus)
if adbConnectionStatus is False:
    print('unable to establish adb connection. Check logs.')
else:
    # start backup process.
    media_mover = Backup()
    backup_summary = media_mover.start_back_up()
    pprint(backup_summary)
