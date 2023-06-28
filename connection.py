# import subprocess
# from pprint import pprint
from utils.utils import Utils
from utils.fileSystemUtils import FileSystemUtils

class Connection:
    def __init__(self):
        self.wslPassword = "784512"
        self.deviceModelNumber = "ZF62226S37"

    def checkUSBConnection(self):
        # Run cmd command to check if device is connected to Windows machine.
        shellCommand = "cmd.exe /C usbipd list"
        shellCommandResult,shell_command_return_code = Utils.runCommand(shellCommand)

        #Above command outputs currently connected and previously connected 
        #devices. We want to check if device is currently connected, hence 
        #splitting the output.
        sections = shellCommandResult.split('\n\n')
        deviceConnected = False # Flag to store device connection state.
        connectedDevice = dict.fromkeys(['BUSID','VID_PID','DEVICE','STATE'],"")

        # Process the "Connected" section.
        connected_lines = sections[0].split('\n')[2:]
        for line in connected_lines:
            busid, vid_pid, *deviceParts, state = line.split()
            device = " ".join(deviceParts)
            print(f'devices list: {device}')
            if "moto" in device:
                deviceConnected = True
                connectedDevice['BUSID'] = busid
                connectedDevice['VID_PID'] = vid_pid
                connectedDevice['DEVICE'] = device
                connectedDevice['STATE'] = state
                break
        return deviceConnected, connectedDevice
    
    def checkWSLAttachment(self, connectedDevice):
        # Checks if USB device is available within the WSL env.
        state = connectedDevice.get('STATE')
        if state.casefold() in ['attached','ubuntu']:
            return True
        else:
            return False
        
    def wslAttachDetach(self, connectedDevice, key="attach"):
        # Attaches USB devices to WSL env.
        busId = connectedDevice.get("BUSID")
        shellCommand = f"cmd.exe /C usbipd wsl {key} -b {busId}"
        shellCommandResult,shell_command_return_code = Utils.runCommand(shellCommand)

        lsUsbCommand = "lsusb"
        Utils.runCommand(lsUsbCommand)
        return shellCommandResult
    
    def adbServer(self):
        # Kill and start adb services as SU. Also list adb devices after 
        # server start.
        killCommand = "sudo -S adb kill-server"
        passwordInput = f"{self.wslPassword}\n"
        killResult,kill_command_return_code = Utils.runCommand(killCommand, input=passwordInput)
        
        startCommand = "sudo adb start-server"
        startResult,start_command_return_code = Utils.runCommand(startCommand)
        
        adbListDevices = "adb devices"
        adbListDevicesResult,adbList_command_return_code = Utils.runCommand(adbListDevices)

        adbConnectionStatus = self.checkAdbConnectionStatus(adbListDevicesResult)
        # return adbListDevicesResult, adbConnectionStatus
        return adbConnectionStatus
    
    def checkAdbConnectionStatus(self,adbListDevicesResult):
        deviceList = adbListDevicesResult.split("\n")
        return any(self.deviceModelNumber in i for i in deviceList)

    # def runCommand(self,command,**kwargs):
    #     # Runs shell command using py subprocess module.
    #     run = subprocess.run(command,shell=True, capture_output=True, text=True,**kwargs)
    #     result = run.stdout
    #     print(f'Shell command result:\n\n------------\n{result}------------')
    #     return result
    
    def establishAdbConnection(self):
        deviceConnectionStatus, connectedDevice = self.checkUSBConnection()
        print(f'Device Connection Status: {deviceConnectionStatus}')
        print(f'Connected Device Details: {connectedDevice}')

        adbConnectionStatus = False
        if deviceConnectionStatus == False:
            # Android phone was not connected to system.
            print("Please connect your Android phone before proceeding")
        else:
            count = 0
            while adbConnectionStatus == False and count < 3:
                print(f"Attempt {count+1} at establishing ADB connection.")
                # Android phone is connected to system, checking WSL attachment.
                connectionState = connectedDevice.get("STATE","")
                status = any(i in connectionState for i in ["ubuntu","attached"])
                if status == True:
                    # Device attached to WSL env. Kill-starting Adb server.
                    print('Device is connected and attached to WSL')
                    adbConnectionStatus = self.adbServer()
                    print(f'Adb Connection Status: {adbConnectionStatus}')
                else:
                    # Device not attached to WSL env. 
                    # Attaching USB device to WSL env and kill-starting Adb server.
                    print("Device is connected but not attached to WSL")
                    self.wslAttachDetach(connectedDevice,"attach")
                    adbConnectionStatus = self.adbServer()
                    print(f'Adb Connection Status: {adbConnectionStatus}')
                
                count += 1

        return adbConnectionStatus

if __name__ == '__main__':
    media = Connection()
    deviceConnectionStatus, connectedDevice = media.checkUSBConnection()
    print(f'Device Connection Status: {deviceConnectionStatus}')
    print(f'Connected Device Details: {connectedDevice}')

    if deviceConnectionStatus == False:
        # Android phone was not connected to system.
        print("Please connect your Android phone before proceeding")
    else:
        # Android phone is connected to system, checking WSL attachment.
        connectionState = connectedDevice.get("STATE","")
        status = any(i in connectionState for i in ["ubuntu","attached"])
        if status == True:
            # Device attached to WSL env. Kill-starting Adb server.
            print('Device is connected and attached to WSL')
            adbConnectionStatus = media.adbServer()
            print(f'Adb Connection Status: {adbConnectionStatus}')
        else:
            # Device not attached to WSL env. 
            # Attaching USB device to WSL env and kill-starting Adb server.
            print("Device is connected but not attached to WSL")
            media.wslAttachDetach(connectedDevice,"attach")
            adbConnectionStatus = media.adbServer()
            print(f'Adb Connection Status: {adbConnectionStatus}')