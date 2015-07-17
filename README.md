# Clover
Clover is a super simple anti-malware for Windows. It aims to stop malware infections in real-time.

Made to be simple. Goes better with common sense.

## Features
* Windows startups registry keys monitoring
* Windows startups files monitoring
* Fake forensis tools, using bait files to detect anti-debugging technics

## Features that will never be implemented
Some features will never be implemented in Clover because they are against Clover's simplicity philosophy:
* Auto updates
* Signature-based detection

## Download
[Clover 1.0](https://github.com/clover-av/clover/blob/master/bin/Clover_Antimalware_1_0_Setup.exe?raw=true)

If you install this software, it means that you have read and accept its GNU General Public License 3. You can read it [here](https://github.com/clover-av/clover/blob/master/LICENSE.md). 

## Minimum requirements
- Windows XP, 7, 8
- 12MB RAM
- 30MB free space in HD

## How to compile?
You gonna need [PyInstaller](https://github.com/pyinstaller/pyinstaller/wiki) and [Python 2.7](https://www.python.org/download/releases/2.7) installed.

Access Clover's *src* folder and run:

    pyinstaller.exe --icon clover.ico --noconsole

To compile bait files, you gonna need g++:

    g++.exe wireshark.exe
