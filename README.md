# AutoMover

I don't like keeping years worth of data on my phone and then dump it all at once in a single folder on my computer or my HDD and god forbid if I ever have to search for something in that backup. I would much rather give up. To counter this I built AutoMover, which is an automation script written in Python that would backup all the data for me and organize it properly without me actually having to do anything.

Currently this script is programmed to run on a system that is a combination of Windows and Linux, but, eventually I may convert it to run solely on Linux or Windows. Make it more plug-n-play. Not a promise, it depends on my need.

**IMPORTANT NOTE**: The source directories might be different depending on the OS. I use a really old device and the new stuff probably works differently, but, just changing the source directories in the ```constants.py``` should work.

Here's the system I'm running:

- Python 3.8.10
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/about)
- Windows 10
- x64 processor
- Ubuntu 20.04 on Windows
- Linux Kernel version: 5.15.90.1
- [USBIPD-WIN](https://github.com/dorssel/usbipd-win)
- [Android Debug Bridge (adb)](https://developer.android.com/tools/adb)
- [USB debugging is enabled on the Android device.](https://developer.android.com/studio/debug/dev-options#Enable-debugging)

In terms of directory structure, it'll be something like this:

```User > Device Name > Year > Month > File Type > Data Source```

For example:

![Directory Structure](/images/tree.png)

I'll be adding documents and other file types at a later stage.

The entire process is divided into 2 main parts:

1. Establishing connection with the Android device via WSL.
2. Backing up the data.

Prerequisites:
- USBIPD-WIN is installed.
- Android Debug Bridge (adb) is installed.
- USB debugging is enabled on the Android device.

<br>

## Accessing phone via WSL

Assuming that you have connected your device, we need to check if it is attached to the WSL environment and if we can access the Adb Shell and its commands. To do that, we do the following:

### In command prompt:
```
$ usbipd list
```
This will give you the list of USB devices connected to your machine and if it is attached to your WSL environment or not. The output will look similar to this:

![uspipd list output](/images/usbipdlist.png)

Notice the "```Shared```" status, that means the device is is connected but not attached to the WSL environment. We achieve that by running the ```usbipd wsl attach``` command.
```
$ usbipd wsl attach --busid <busid>
```
This command doesn't return an output, so to check if the device is attached, we run the first command again and get the following output:

![uspipd list attached output](/images/usbipdlistattached.png)

we can also check this by running the ```lsusb``` command in the WSL shell, which gives the output:

![lsusb](/images/lsusb.png)

If you don't see your device here, redo the above steps and see if you have written the correct bus id.

Now that the device is attached to the WSL environment, we can move on to gaining access to the adb shell. What I've noticed is that in case we have previously started the adb server, we still sometimes have access to the adb shell. This only happens sometimes and is unpredictable. So, I manually kill and restart the server.

### In WSL:
```
$ sudo adb kill-server
$ sudo adb start-server
$ adb devices
$ adb shell
```
Executing ```adb devices``` on WSL should give you an outcome similar to the one below:

![adb devices](/images/adbdevices.png)

The "ZF62226S37" you see is the model number of the Android device I'm using. You'll find the same model number in "device info" of your Android smartphone. 

The [connection.py](https://github.com/ashrithzxy/AutoMover/blob/main/connection.py) is responsible for establishing the connection between the Android device and the WSL environment and gaining access to the shell.

With this, we have everything we need to start moving files from the phone to our local machine. The command we'll be using to move files across is the ```adb pull``` command that has the following format:

```
$ adb pull /path/to/phone/file /path/to/wsl/destination
```

## Code

The codebase is divided into 3 main sections:
- [backup.py](https://github.com/ashrithzxy/AutoMover/blob/main/backup.py) : takes care of moving the data across and organizing it.
- [utils](https://github.com/ashrithzxy/AutoMover/tree/main/utils) : Classes that help with running shell commands and creating directories.

## Backing up the data:

This is performed in 2 stages:

1. Creation of folders on the local system into which the data will be backed up.
2. Copying the data from the device to the local system.

### Preparing backup folders:

Initially, I would check if the correct folder existed, and if it didn't, I would create it, but this meant running a lot of  ```find``` and ```mkdir``` commands. This was how I used to do it: 

```python
current_year = dt.now().year

'''Check if required directory already exists.'''
command = f"find {parent_dir_path} -type d -path '{dirname}'"
command_execute, command_return_code = Utils.runComman(command)

if bool(command_return_code) is False:
    '''Required directory doesn't already exist. Create a new directory.'''
    mkdir_command = f"mkdir -p {parent_dir_path}{dirname}"
    execute_mkdir_command, mkdir_command_return_code = Utils.runCommand(mkdir_command)
```
The above method could only find one directory at a time and could only make one directory at a time as well. This worked all right, as long as all the directories we created once, but it still doesn't make much sense to check them one by one. 

Now, I use the following to create all the required directories:

```
"bash -c 'mkdir -p ~/AutoMoverBackup/2025/June/Images/{Whatsapp,Instagram,Snapseed}'"
```
The number of commands I need to execute to create all required directories is equal to the number of file types I want to back up. The ```mkdir -p``` command makes parent directories as needed, and it does not throw an error if a directory already exists, which means I could create multiple directories at once. 

The ``` {Whatsapp,Instagram,Snapseed} ``` part of the command is called brace expansion. With this, I can create multiple subdirectories inside the /Images (or any other file type) directory. 

There was one problem, though. You see, I was using Python's ```subprocess``` module to execute these commands, and it seems like it doesn't support brace expansions. Brace expansion is a feature provided by the shell, and it is not directly supported by the subprocess.run function in Python. The solution was to run the command via the shell using ```bash -c```, allowing you to leverage shell features, such as brace expansion, before executing the command. 

Once this was figured out, all the required directories were ready, and we could start the backup process. 

### Create backup

We needed to back up only those files that were created this month and leave everything else untouched. This meant matching the file names with the current year and month. Most files had a common prefix and a common format, something like ```IMG-YYYYMM``` or ```VID_YYYYMM```. I needed to use the ```find``` command to locate only files and pull only those files that matched this pattern. Here's the command that I used; it looks a bit messy, but, it makes sense:

```
adb shell find SOURCE -type f | grep PATTERN | xargs -I {} adb pull {} DESTINATION
```
The breakdown of this is as follows: 
1. We start the interactive shell on Android devices using ```adb shell``
2. Then, using ```find```, we search for files inside the SOURCE directory while restricting the search to only files using ```-type f```.
3. The output of the find command is redirected to the ```grep``` command, which filters out the files that don't match the predefined pattern.
4. The output of the grep command, which is a list of file names, is then redirected to ```xargs -I {}```, which replace the ```{}``` in the ```adb pull {} DESTINATION``` command with individual file names, which are then copied from the phone to the local machine, thus creating a backup.

Currently, I'm backing up images, audio and video from internal storage only. In future updates, I'll backup data from the external storage as well and add support for other file types as well. I also want to add a progress bar. That would look cool.

NOTES:
- In the adb shell, the sd card is referred to as internal storage, and the external storage can be found at storage > 211D-190C. The "211D-190C" will probably be something else for you, but should be something similar.
