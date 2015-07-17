[Setup]
AppName=Clover Antimalware
AppVersion=1.1
DefaultDirName={pf}\Clover
DefaultGroupName=Clover
UninstallDisplayIcon={app}\clover.exe
Compression=lzma2
SolidCompression=yes
OutputDir=C:\Python27\dist\
PrivilegesRequired=admin

[Files]
Source: "C:\Python27\dist\clover\*"; DestDir: "{app}"; Flags: recursesubdirs; Excludes: "*.iss"

[Run]
Filename: "{app}\clover.exe"; Parameters: "--install" ; Flags: runhidden
Filename: "{app}\clover_monitor.exe"; Parameters: "--startup auto --interactive install" ; Flags: runhidden

[UninstallRun]
Filename: "{app}\clover_monitor.exe"; Parameters: "stop" ; Flags: runhidden
Filename: "{app}\clover_monitor.exe"; Parameters: "delete" ; Flags: runhidden

[Icons] 
Name: "{commonstartup}\Clover"; Filename: "{app}\clover.exe"

[Registry]
Root: HKLM; Subkey: "Software\Clover"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Clover\Settings"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"