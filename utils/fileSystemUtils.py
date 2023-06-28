import os
from datetime import datetime as dt
from .utils import Utils

class FileSystemUtils:
    """Class to help with creating and organizing directories."""
    BACKUP_LOCATION = "~/AutoMoverBackup/"
    def __init__(self):
        pass

    @staticmethod
    def check_and_create_directory(parent_dir_path, dirname):
        """Checks if a dir corresponding to creent year exists in the backup 
        location. If not, creates it."""
        current_year = dt.now().year

        find_directory_command = f"find {parent_dir_path} -type d -path '{dirname}'"
        find_directory_command_execute, find_directory_command_return_code = Utils.runCommand(find_directory_command)

        if bool(find_directory_command_execute) is False:
            print(f"directory named '{dirname}' does not exist. Creating.")
            mkdir_command = f"mkdir -p {parent_dir_path}{dirname}"
            execute_mkdir_command, mkdir_command_return_code = Utils.runCommand(mkdir_command)
            if mkdir_command_return_code == 0:
                return True 
            else:
                return False
        print(f"directory named '{dirname}' already exists.")
        return True

if __name__ == "__main__":
    print(FileSystemUtils.check_and_create_directory(FileSystemUtils.BACKUP_LOCATION,dt.now().year))