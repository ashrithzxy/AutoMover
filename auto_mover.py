from connection import Connection
from backup import Backup
from pprint import pprint

device = Connection()
adb_connection_status = device.establish_adb_connection()
print("Adb Connection Status is: ",adb_connection_status)
if adb_connection_status is False:
    print('unable to establish adb connection. Check logs.')
else:
    # start backup process.
    media_mover = Backup()
    backup_summary = media_mover.start_back_up()
    pprint(backup_summary)
