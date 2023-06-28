from utils.utils import Utils

class Backup:
    def __init__(self):
        self.backupLocation = '~/motoG6Backup/backup/'

    def moveToLocal(self, source, destination):
        pass

    def organize(self):
        pass

    def createBackup(self):
        """
        Creates a backup of device media from Whatsapp, Camera, Snapseed, 
        Instagram etc.
        """        
        pass

    def images(self):
        pass

    def videos(self):
        pass

    def documents(self):
        pass

    def audio(self):
        pass

    def whatsapp(self):
        timestampPattern = "YYYYMMDD"

        imageSource = "/sdcard/WhatsApp/Media/WhatsApp\ Images/"
        imageFileNameBasePattern = "IMG-"
        imageDestination = ""

        videoSource = "/sdcard/WhatsApp/Media/WhatsApp\ Video/"
        videoFileNameBasePattern = "VID-"
        videoDestination = ""

        audioSource = "/sdcard/WhatsApp/Media/WhatsApp\ Audio/"
        audioFileNameBasePattern = "AUD-"
        audioDestination = ""

    def snapseed(self):
        source = "/sdcard/Snapseed/"
        fileNamePattern = "IMG_"
        timestampPattern = "YYYYMMDD"
        destination = ""

    def camera(self):
        imageSource = "/DCIM/Camera/"
        imageFileNamePattern = "IMG_"
        timestampPattern = "YYYYMMDD"
        imageDestination = ""

        videoSource = "/DCIM/Camera/"
        videoFileNamePattern = "VID_"
        timestampPattern = "YYYYMMDD"
        videoDestination = ""

    def pictures(self):
        """
        Probably best to cycle through subdirs and compare creation dates of files.
        """        
        pass

    def getFileNamePattern(self,baseString):
        pass

if __name__ == '__main__':
    backupHelper = Backup()
    # backupHelper.moveToLocal()