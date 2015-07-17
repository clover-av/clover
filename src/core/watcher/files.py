from threading import Thread
from time import sleep
import winshell
import glob

class files(Thread):
	def __init__(self,gui,folder,timeout=5):
		Thread.__init__(self)
		self.folder = folder
		self.timeout = timeout
		self.gui = gui
		self.files_old = self.files()

	def files(self):
		return glob.glob(self.folder+"\*")

	def run(self):
		while True:
			files_now = self.files()
			for file_now in files_now:
				if file_now not in self.files_old:
					self.gui.q.put((self.gui.changed_file, (file_now, ), {}))
			self.files_old = files_now
			sleep(self.timeout)

	@staticmethod
	def startups():
		return [winshell.startup(), winshell.startup(1)]
	