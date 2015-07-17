from threading import Thread
from time import sleep
import winshell
import glob, subprocess

class process(Thread):
	def __init__(self,gui,process,timeout=60):
		Thread.__init__(self)
		self.process = process
		self.timeout = timeout
		self.gui = gui
		self.stopped = False

	def files(self):
		return glob.glob(self.folder+"\*")

	def run(self):
		sleep(self.timeout)
		while self.stopped is not True:
			proc_list = subprocess.Popen('tasklist.exe /fo csv', stdout=subprocess.PIPE, universal_newlines=True).stdout
			if not self.process in proc_list:
				self.gui.q.put((self.gui.changed_process, (self.process, ), {}))
				self.stopped = True
			sleep(self.timeout)