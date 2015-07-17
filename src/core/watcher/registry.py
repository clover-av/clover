import win32api
import win32event
import win32con
import _winreg
import win32file

class registry:
	def __init__(self, gui, keys, timeout=1):
		""" Creates a thread and sets parameters
		gui:	CloverServiceInterface
		keys:	Registry keys to be monitored
		"""
		self.keys = keys
		self.gui = gui
		self.timeout = timeout
		self.keys_old = []
		self.whitelist = []
		# sets keys_old size to the same as keys size
		for i in range(len(keys)):
			self.keys_old.append([])
		
	def list(self, key, hkey):
		""" Returns registry key values """
		win_key = _winreg.OpenKey(hkey, key, 0, _winreg.KEY_READ)
		keys = []
		try: # QueryInfoKey does not work
			i = 0
			while True:
				keys.append(_winreg.EnumValue(win_key, i))
				i = i + 1
		except WindowsError:
		    pass
		_winreg.CloseKey(win_key)
		return keys

	def start(self):
		""" Populates old_keys list with updated values """
		keys_list = [] 
		for key in self.keys:
			keys_now = self.list(key[1], self.hkey(key[0]))
			keys_list.append(keys_now)
		self.keys_old = keys_list

	def restore(self, changed_key, changed_value, keys):
		for key in keys:
			if key[0] == changed_value[0]:
				self.whitelist.append(key)

				regkey = _winreg.OpenKey(self.hkey(changed_key[0]), changed_key[1], 0, _winreg.KEY_WRITE)
				_winreg.SetValueEx(regkey, key[0], 0, _winreg.REG_SZ, key[1])
				_winreg.CloseKey(regkey)

				return True
		# key did not exist before, so it must be deleted
		regkey = _winreg.OpenKey(self.hkey(changed_key[0]), changed_key[1], 0, _winreg.KEY_WRITE)
		_winreg.DeleteValue(regkey, changed_value[0])
		_winreg.CloseKey(regkey)

	def run(self):
		""" Thread started, runs monitor """
		keys_list = [] # stores actual values
		for key in self.keys:
			keys_now = self.list(key[1], self.hkey(key[0]))
			keys_list.append(keys_now)

		i = 0
		# compares keys
		for key in keys_list:
			for value in key:
				if value not in self.keys_old[i] and value not in self.whitelist:
					# sends whole keys_old because it may had its order changed
					self.gui.changed_key(value, self.keys[i], self.keys_old[i])
			i = i + 1

		self.keys_old = keys_list # refresh old values'''
		# self.whitelist = [] # bug

	@staticmethod
	def hkey(name):
		""" Gets _winreg HKEY constraint """
		name = name.upper()
		winreg_hkey = None
		# https://docs.python.org/2/library/_winreg.html#hkey-constants
		if name == 'HKLM':
			winreg_hkey = _winreg.HKEY_LOCAL_MACHINE
		elif name == 'HKCU':
			winreg_hkey = _winreg.HKEY_CURRENT_USER
		elif name == 'HKU':
			winreg_hkey = _winreg.HKEY_USERS
		else:
			raise Exception("Invalid HKEY")

		return winreg_hkey

	@staticmethod
	def list_keys(key):
		""" Returns a list with keys subkeys """
		whkey, wkey = key
		whkey = registry.hkey(whkey)
		regkey = _winreg.OpenKey(whkey, wkey, 0, _winreg.KEY_READ)
		keys = []
		try:
			i = 0
			while True:
				subkey = _winreg.EnumKey(regkey, i)
				keys.append(subkey)
				i = i + 1
		except WindowsError:
			pass
		return keys

	@staticmethod
	def key_exists(key):
		""" Returns True if key exists """
		whkey, wkey = key
		whkey = registry.hkey(whkey)
		try:
			regkey = _winreg.OpenKey(whkey, wkey, 0, _winreg.KEY_WRITE)
			_winreg.CloseKey(regkey)
			return True
		except:
			return False

	@staticmethod
	def key_value(key):
		""" Returns False if key does not exists or its value """
		whkey, wkey = key
		whkey = registry.hkey(whkey)
		try:
			regkey = _winreg.OpenKey(whkey, wkey, 0, _winreg.KEY_READ)
			val = _winreg.QueryValueEx(regkey, "InstallPath")
			_winreg.CloseKey(regkey)
			return val
		except:
			return False