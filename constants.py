BACKUP_LOCATION = "~/AutoMoverBackup/"
WHATSAPP_MEDIA_BASEPATH = "/sdcard/WhatsApp/Media/WhatsApp\ "
SNAPSEED_MEDIA_BASEPATH = "/sdcard/Snapseed/"
DCIM_MEDIA_BASEPATH = "/sdcard/DCIM/Camera/"
PICTURES_MEDIA_BASEPATH = "/sdcard/Pictures/"
BACKUP_COMMAND = 'adb shell find "{}" -type f | grep "{}" | xargs -I {} adb pull {} {}'
ADB_TEST = "My name is {}, I am a {}, I am {} {} years old {}."
MOTOG6 = "ZF62226S37"