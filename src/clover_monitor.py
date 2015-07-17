# -*- coding: utf8 -*-
from core.service import AppServerSvc
import win32serviceutil
import servicemanager

VERSION = "1.1"
NAME = "Clover AntiMalware"

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
