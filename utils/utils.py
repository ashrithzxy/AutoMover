import subprocess
from datetime import datetime as dt

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def runCommand(command,**kwargs):
        # Runs shell command using py subprocess module.
        run = subprocess.run(command,shell=True, capture_output=True, text=True, check=False, **kwargs)
        result = run.stdout
        return_code = run.returncode
        print(f'\n>>>Command: {command}')
        print(f'>>>Shell command result:\n\n------------\n{result}------------')
        return result, return_code
    

    @staticmethod
    def get_month_name(dtObject, ):
        pass
