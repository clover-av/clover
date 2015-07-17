from interface.CloverInterface import CloverServiceInterface
from watcher.registry import registry
from watcher.files import files
from settings import settings
import sys, os, time, subprocess
import win32serviceutil
import servicemanager
import win32process
import win32service
import win32event
import win32api
import win32con
import socket
import json

DETACHED_PROCESS = 0x00000008

class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "CloverMonitorA"
    _svc_display_name_ = "CloverMonitorA"
    _stoped = False

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self._stoped = True

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()

    def read_blocks(self,queue):
        try:
            pipe_back = open(queue, "r")
            queue = pipe_back.readlines()
            pipe_back.close()
            return queue
        except:
            return ''

    def run_capado(self,exec_file):
        startup_info = win32process.STARTUPINFO()
        startup_info.dwFlags = win32process.STARTF_USESHOWWINDOW
        win32process.CreateProcess(None, exec_file, None, None, 0, win32process.REALTIME_PRIORITY_CLASS, None, None, startup_info)

    def main(self):
        servicemanager.LogInfoMsg("Clover Monitor Exterminator is up and running!")
        self.run_capado(settings.setup_path()+'\\wireshark.exe')

        pipe_path = settings.pipe_path() # out
        in_path = settings.pipe_path(2)
        service_notifier = CloverServiceInterface(pipe_path=pipe_path) # interface sends to out pipe
        # current_user does not exists in the service context
        watched_keys = [('HKLM', 'Software\Microsoft\Windows\CurrentVersion\Run'),
                        ('HKLM', 'Software\Microsoft\Windows\CurrentVersion\RunOnce')]
        users = registry.list_keys(('HKU', ''))
        for user in users:
            if registry.key_exists(('HKU', str(user) + '\Software\Microsoft\Windows\CurrentVersion\Run')) is not False:
                watched_keys.append(('HKU', str(user) + '\Software\Microsoft\Windows\CurrentVersion\Run'))
            if registry.key_exists(('HKU', str(user) + '\Software\Microsoft\Windows\CurrentVersion\RunOnce')) is not False:
                watched_keys.append(('HKU', str(user) + '\Software\Microsoft\Windows\CurrentVersion\RunOnce'))

        registry_watcher = registry(service_notifier, watched_keys)
        registry_watcher.start()
        while True: 
            if self._stoped:
                break
            # check if is there anything to process
            queue = self.read_blocks(in_path)
            processed = []
            for block in queue:
                block = json.loads(block)
                if block['type'] == 1:
                    processed.append(block)
                    registry_watcher.restore(block['key'], block['changed_value'], block['keys_old'])
            # re-reads blocks and then subtracks the ones that were processed
            queue = self.read_blocks(in_path)
            pipe_back = open(in_path, "w")
            for block in queue:
                block = json.loads(block)
                if block not in processed:
                    block = json.dumps(block)
                    pipe_back.write(block + "\n")
            pipe_back.close()

            registry_watcher.run()
            time.sleep(5)
            pass