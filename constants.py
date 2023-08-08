BACKUP_LOCATION = "~/AutoMoverBackup/"
WHATSAPP_MEDIA_BASEPATH = "/sdcard/WhatsApp/Media/WhatsApp\ "
SNAPSEED_MEDIA_BASEPATH = "/sdcard/Snapseed/"
DCIM_MEDIA_BASEPATH = "/sdcard/DCIM/Camera/"
EXTERNAL_DCIM_MEDIA_BASEPATH = "/storage/211D-190C/DCIM/Camera/"
PICTURES_MEDIA_BASEPATH = "/sdcard/Pictures/"
BACKUP_COMMAND = 'adb shell find "{}" -type f | grep "{}" | xargs -I {} adb pull {} {}'
MOTOG6 = "ZF62226S37"