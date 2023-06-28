BACKUP_LOCATION = "~/AutoMoverBackup/"
WHATSAPP_MEDIA_BASEPATH = "/sdcard/WhatsApp/Media/WhatsApp\ "
BACKUP_COMMAND = 'adb shell find "{}" -type f | grep "{}" | xargs -I {} adb pull {} {}'
ADB_TEST = "My name is {}, I am a {}, I am {} {} years old {}."
