from .utils import Utils

class FileSystemUtils:
    """Class to help with creating and organizing directories."""
    BACKUP_LOCATION = "~/AutoMoverBackup/"
    def __init__(self):
        pass

    @staticmethod
    def check_and_create_directory(parent_dir_path=None, dirname=None, direct_bash=False, direct_command=None):
        """Creates required backup directories. Makes parent dirs as needed 
        using the -p flag with mkdir. 

        Returns:
            Bool: True if return code is 0(Command executed without any errors.), 
                  False is return code is 1(Error during command execution).
        """        
        # sample_command = "bash -c 'mkdir -p ~/AutoMoverBackup/2025/June/Images/{Whatsapp,Instagram,Snapseed}'"
        mkdir_command = direct_command
        execute_mkdir_command, mkdir_command_return_code = Utils.run_command(mkdir_command)
        return not bool(mkdir_command_return_code)

if __name__ == "__main__":
    location = "~/AutoMoverBackup/2029/June/Images/{Whatsapp,Instagram,Snapseed}"
    format = "Images/"
    dirname = "{Whatsapp,Instagram,Snapseed}"
    # dirname = "2029/June/Images/{Whatsapp,Instagram,Snapseed}"
    # FileSystemUtils.BACKUP_LOCATION,dt.now().year)
    print(FileSystemUtils.check_and_create_directory(location,format,dirname))