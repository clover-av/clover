from watcher.registry import registry
import winshell

class settings:
	@staticmethod
	def setup_path():
		ckey = registry.key_value(('HKLM', 'Software\Clover\Settings'))
		if ckey is False:
			raise Exception("Invalid installation")
		return ckey[0]

	@staticmethod
	def pipe_path(to=1):
		pipe_file = 'back'
		if to != 1:
			pipe_file = 'front'
		return winshell.application_data(1) + '\\pipe_' + pipe_file + '.js' 
