from pprint import pprint
from utils.utils import Utils
from utils.file_system_utils import FileSystemUtils
import constants
from datetime import datetime as dt

class Backup:
    def __init__(self):
        self.device_owner = "Ashrith"
        self.device_name = "MotorolaG6"
        self.backup_dir = f"{constants.BACKUP_LOCATION}{self.device_owner}/{self.device_name}/"
        self.now = dt.now()
        self.strftime_pattern = "%Y%m"
        self.current_year  = self.now.year
        self.current_month_name = self.now.strftime("%B")
        self.year_dir_path = f"{self.backup_dir}{self.current_year}/"
        self.current_month_backup_dir = self.year_dir_path + self.current_month_name + "/"
        self.backup_summary = {
            "images":{
                "whatsapp":False,
                "instagram":False,
                "camera":False,
                "screenshots":False,
                "snapseed":False
            },
            "audio":
            {
                "whatsapp":False
             },
            "video":{
                "whatsapp":False,
                "camera":False
                },
            "error":None
        }

    def create_backup(self, source=None, destination=None, pattern=None, **kwargs):
        """
        Creates a backup of device media from Whatsapp, Camera, Snapseed, 
        Instagram etc.
        """
        #adb shell find "/sdcard/WhatsApp/Media/WhatsApp\ Images/" -type f 
        # | grep "IMG-202306" 
        # | xargs -I {} adb pull {} ~/motoG6Backup/backup/
        backup_command = constants.BACKUP_COMMAND.format(source,pattern,"{}","{}",destination)
        backup_command_execute, backup_command_return_code = Utils.run_command(backup_command)
        return not bool(backup_command_return_code)

        # return "current year and month dir ready for backup"
    
    def prepare_directories(self):
        """Creates required directories for storing data.

        Returns:
            Bool: True if all req dirs are created successfully else False.
        """        
        command_list = self.create_direct_command()
        return_code = False
        for command in command_list:
            bash_command = f"bash -c 'mkdir -p {command}'"
            # NOTE: using bach -c because subprocess.run doesn't seem to 
            # support brace expansion which we are using to make multiple 
            # directories at once and creatin their parents as needed.
            return_code = FileSystemUtils.check_and_create_directory(direct_bash=True,direct_command=bash_command)
            if return_code is False:
                break
        
        return return_code
    
    def create_direct_command(self):
        """Creates a list containing filepaths for backup dirs to be created.

        Returns:
            List: Contains list of filepaths.
        """        
        command_list = []
        command_list.append(self.current_month_backup_dir + "Images/{Whatsapp,Snapseed,Instagram,Camera,Screenshots}")
        command_list.append(self.current_month_backup_dir + "Audio/Whatsapp")
        command_list.append(self.current_month_backup_dir + "Video/{Whatsapp,Camera}")
        return command_list

    def whatsapp(self):
        """Creates backup of Whatsapp images, audio and videos.
        """

        # Backing up Whatsapp Images
        image_source = constants.WHATSAPP_MEDIA_BASEPATH + "Images/"
        image_file_name_base_pattern = "IMG-"
        image_file_name_pattern = image_file_name_base_pattern + self.now.strftime(self.strftime_pattern)
        image_destination = f"{self.current_month_backup_dir}/Images/Whatsapp/" 
        image_backup_result = self.create_backup(image_source,image_destination,image_file_name_pattern)
        self.backup_summary["images"]["whatsapp"] = image_backup_result

        # Backing up Whatsapp Audio, not voice notes
        audio_source = constants.WHATSAPP_MEDIA_BASEPATH + "Audio/"
        audio_file_name_base_pattern = "AUD-"
        audio_file_name_pattern = audio_file_name_base_pattern + self.now.strftime(self.strftime_pattern)
        audio_destination = f"{self.current_month_backup_dir}/Audio/Whatsapp/" 
        audio_backup_result = self.create_backup(audio_source,audio_destination,audio_file_name_pattern)
        self.backup_summary["audio"]["whatsapp"] = audio_backup_result

        # Backing up Whatsapp Videos
        video_source = constants.WHATSAPP_MEDIA_BASEPATH + "Video/"
        video_file_name_base_pattern = "VID-"
        video_file_name_pattern = video_file_name_base_pattern + self.now.strftime(self.strftime_pattern)
        video_destination = f"{self.current_month_backup_dir}/Video/Whatsapp/" 
        video_backup_result = self.create_backup(video_source,video_destination,video_file_name_pattern)
        self.backup_summary["video"]["whatsapp"] = video_backup_result

    def snapseed(self):
        """Creates backup of Snapseed images.
        """        
        image_source = constants.SNAPSEED_MEDIA_BASEPATH
        image_file_name_base_pattern = "IMG_"
        image_file_name_pattern = image_file_name_base_pattern + self.now.strftime(self.strftime_pattern)
        image_destination = f"{self.current_month_backup_dir}/Images/Snapseed/" 
        image_backup_result = self.create_backup(image_source,image_destination,image_file_name_pattern)
        self.backup_summary["images"]["snapseed"] = image_backup_result

    def camera(self):
        """Creates backup of Camera images and videos.
        """

        media_source = constants.DCIM_MEDIA_BASEPATH
        
        image_file_name_base_pattern = "IMG_"
        image_file_name_pattern = image_file_name_base_pattern + self.now.strftime(self.strftime_pattern)
        image_destination = f"{self.current_month_backup_dir}/Images/Camera/" 
        image_backup_result = self.create_backup(media_source,image_destination,image_file_name_pattern)
        self.backup_summary["images"]["camera"] = image_backup_result

        video_file_name_base_pattern = "VID_"
        video_file_name_pattern = video_file_name_base_pattern + self.now.strftime(self.strftime_pattern)
        video_destination = f"{self.current_month_backup_dir}/Video/Camera/" 
        video_backup_result = self.create_backup(media_source,video_destination,video_file_name_pattern)
        self.backup_summary["video"]["camera"] = video_backup_result

    def pictures(self):
        """
        Creates backup of images in the "Pictures" folder of internal storage.
        This is where screenshots, instagram images are.
        """

        pictures_sub_dir_dict = {"Instagram":"IMG_","Screenshots":"Screenshot_"}
        for dir_name, base_pattern in pictures_sub_dir_dict.items():
            image_source = constants.PICTURES_MEDIA_BASEPATH + f"{dir_name}/"
            image_file_name_pattern = base_pattern + self.now.strftime(self.strftime_pattern)
            image_destination = f"{self.current_month_backup_dir}/Images/{dir_name}/" 
            return_code = self.create_backup(image_source,image_destination,image_file_name_pattern)
            self.backup_summary['images'][dir_name.casefold()] = return_code 

    def start_back_up(self):
        backup_dir_status = self.prepare_directories()
        if backup_dir_status is False:
            self.backup_summary["error"] = "Backup directories not ready. Aborting backup process. Check logs"
            self.backup_summary["status"] = False
            return self.backup_summary
        else:
            self.whatsapp()
            self.snapseed()
            self.camera()
            self.pictures()
            self.backup_summary["status"] = True
        
        return self.backup_summary

if __name__ == '__main__':
    backup_helper = Backup()

    backup_dir_status = backup_helper.prepare_directories()
    if backup_dir_status is False:
        print("Backup destination not ready. Aborting backup process.")
    else:
        backup_helper.whatsapp()
        backup_helper.snapseed()
        backup_helper.camera()
        backup_helper.pictures()
    
    pprint(backup_helper.backup_summary)
