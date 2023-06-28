from utils.utils import Utils
from utils.fileSystemUtils import FileSystemUtils
import constants
from datetime import datetime as dt

class Backup:
    def __init__(self):
        self.backup_dir = constants.BACKUP_LOCATION
        self.now = dt.now()

    def moveToLocal(self, source, destination):
        pass

    def organize(self):
        pass

    def createBackup(self, source=None, destination=None, pattern=None, **kwargs):
        """
        Creates a backup of device media from Whatsapp, Camera, Snapseed, 
        Instagram etc.
        """
        backup_dir_status = self.prepare_directories()
        if backup_dir_status is False:
            return "Backup destination not ready. Aborting backup process."

        backup_command = constants.BACKUP_COMMAND.format(source,pattern,"{}","{}",destination)
        Utils.runCommand(backup_command)

        # return "current year and month dir ready for backup"
    
    def prepare_directories(self):

        current_year  = self.now.year
        create_year_dir = FileSystemUtils.check_and_create_directory(self.backup_dir,current_year)
        if create_year_dir is False:
            return False
        
        current_month = self.now.strftime("%B")
        year_dir_path = f"{self.backup_dir}{current_year}/"
        create_month_dir = FileSystemUtils.check_and_create_directory(year_dir_path,current_month)
        if create_month_dir is False:
            return False

        # whatsapp_images_subdir = "/"
        # whatsapp_videos_subdir = 
        # whatsapp_audio_subdir = 

        return True

    def whatsapp(self):
        strftime_pattern = "%Y%m"
        image_source = constants.WHATSAPP_MEDIA_BASEPATH + "Images/"
        image_file_name_base_pattern = "IMG-"
        file_name_pattern = image_file_name_base_pattern + self.now.strftime(strftime_pattern)
        image_destination = self.backup_dir + "2023/June/"
        self.createBackup(image_source,image_destination,file_name_pattern)

        # videoSource = "/sdcard/WhatsApp/Media/WhatsApp\ Video/"
        # videoFileNameBasePattern = "VID-"
        # videoDestination = ""

        # audioSource = "/sdcard/WhatsApp/Media/WhatsApp\ Audio/"
        # audioFileNameBasePattern = "AUD-"
        # audioDestination = ""
        return None

    def snapseed(self):
        source = "/sdcard/Snapseed/"
        file_name_pattern = "IMG_"
        timestampPattern = "YYYYMMDD"
        destination = ""

    def camera(self):
        imageSource = "/DCIM/Camera/"
        imagefile_name_pattern = "IMG_"
        timestampPattern = "YYYYMMDD"
        imageDestination = ""

        videoSource = "/DCIM/Camera/"
        videofile_name_pattern = "VID_"
        timestampPattern = "YYYYMMDD"
        videoDestination = ""

    def pictures(self):
        """
        Probably best to cycle through subdirs and compare creation dates of files.
        """        
        pass

    def getfile_name_pattern(self,baseString):
        pass

if __name__ == '__main__':
    backupHelper = Backup()
    # print(backupHelper.createBackup())
    print(backupHelper.whatsapp())
