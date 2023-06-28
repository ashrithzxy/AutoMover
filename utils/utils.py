import subprocess

class Utils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def runCommand(command,**kwargs):
        # Runs shell command using py subprocess module.
        run = subprocess.run(command,shell=True, capture_output=True, text=True, check=False, **kwargs)
        result = run.stdout
        print(f'\n>>>Command: {command}')
        print(f'>>>Shell command result:\n\n------------\n{result}------------')
        return result
