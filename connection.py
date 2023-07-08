import os
from utils.utils import Utils
from utils.file_system_utils import FileSystemUtils
import constants

class Connection:
    def __init__(self):
        self.wsl_password = os.environ.get("AUTOMOVER_PASS")
        self.device_model_number = constants.MOTOG6
        self.device_name = "moto"

    def check_usb_connection(self):
        # Run cmd command to check if device is connected to Windows machine.
        shell_command = "cmd.exe /C usbipd list"
        shell_command_result,shell_command_return_code = Utils.run_command(shell_command)

        #Above command outputs currently connected and previously connected 
        #devices. We want to check if device is currently connected, hence 
        #splitting the output.
        sections = shell_command_result.split('\n\n')
        device_connected = False # Flag to store device connection state.
        connected_device = dict.fromkeys(['BUSID','VID_PID','DEVICE','STATE'],"")

        # Process the "Connected" section.
        connected_lines = sections[0].split('\n')[2:]
        for line in connected_lines:
            bus_id, vid_pid, *device_parts, state = line.split()
            device = " ".join(device_parts)
            print(f'devices list: {device}')
            if self.device_name in device:
                device_connected = True
                connected_device['BUSID'] = bus_id
                connected_device['VID_PID'] = vid_pid
                connected_device['DEVICE'] = device
                connected_device['STATE'] = state
                break
        return device_connected, connected_device
    
    def check_wsl_attachment(self, connected_device):
        # Checks if USB device is available within the WSL env.
        state = connected_device.get('STATE')
        if state.casefold() in ['attached','ubuntu']:
            return True
        else:
            return False
        
    def wsl_attach_detach(self, connected_device, key="attach"):
        # Attaches USB devices to WSL env.
        busId = connected_device.get("BUSID")
        shell_command = f"cmd.exe /C usbipd wsl {key} -b {busId}"
        shell_command_result,shell_command_return_code = Utils.run_command(shell_command)

        ls_usb_command = "lsusb"
        Utils.run_command(ls_usb_command)
        return shell_command_result
    
    def abd_server(self):
        # Kill and start adb services as SU. Also list adb devices after 
        # server start.
        kill_command = "sudo -S adb kill-server"
        password_input = f"{self.wsl_password}\n"
        kill_result,kill_command_return_code = Utils.run_command(kill_command, input=password_input)
        
        start_command = "sudo adb start-server"
        start_result,start_command_return_code = Utils.run_command(start_command)
        
        adb_list_devices = "adb devices"
        adb_list_devices_result,adbList_command_return_code = Utils.run_command(adb_list_devices)

        adb_connection_status = self.check_adb_connection_status(adb_list_devices_result)
        # return adb_list_devices_result, adb_connection_status
        return adb_connection_status
    
    def check_adb_connection_status(self,adb_list_devices_result):
        device_list = adb_list_devices_result.split("\n")
        return any(self.device_model_number in i for i in device_list)
    
    def establish_adb_connection(self):
        device_connection_status, connected_device = self.check_usb_connection()
        print(f'Device Connection Status: {device_connection_status}')
        print(f'Connected Device Details: {connected_device}')

        adb_connection_status = False
        if device_connection_status == False:
            # Android phone was not connected to system.
            print("Please connect your Android phone before proceeding")
        else:
            count = 0
            while adb_connection_status == False and count < 3:
                print(f"Attempt {count+1} at establishing ADB connection.")
                # Android phone is connected to system, checking WSL attachment.
                connection_state = connected_device.get("STATE","")
                status = any(i in connection_state for i in ["ubuntu","attached"])
                if status == True:
                    # Device attached to WSL env. Kill-starting Adb server.
                    print('Device is connected and attached to WSL')
                    adb_connection_status = self.abd_server()
                    print(f'Adb Connection Status: {adb_connection_status}')
                else:
                    # Device not attached to WSL env. 
                    # Attaching USB device to WSL env and kill-starting Adb server.
                    print("Device is connected but not attached to WSL")
                    self.wsl_attach_detach(connected_device,"attach")
                    adb_connection_status = self.abd_server()
                    print(f'Adb Connection Status: {adb_connection_status}')
                
                count += 1

        return adb_connection_status

if __name__ == '__main__':
    media = Connection()
    device_connection_status, connected_device = media.check_usb_connection()
    print(f'Device Connection Status: {device_connection_status}')
    print(f'Connected Device Details: {connected_device}')

    if device_connection_status == False:
        # Android phone was not connected to system.
        print("Please connect your Android phone before proceeding")
    else:
        # Android phone is connected to system, checking WSL attachment.
        connection_state = connected_device.get("STATE","")
        status = any(i in connection_state for i in ["ubuntu","attached"])
        if status == True:
            # Device attached to WSL env. Kill-starting Adb server.
            print('Device is connected and attached to WSL')
            adb_connection_status = media.abd_server()
            print(f'Adb Connection Status: {adb_connection_status}')
        else:
            # Device not attached to WSL env. 
            # Attaching USB device to WSL env and kill-starting Adb server.
            print("Device is connected but not attached to WSL")
            media.wsl_attach_detach(connected_device,"attach")
            adb_connection_status = media.abd_server()
            print(f'Adb Connection Status: {adb_connection_status}')