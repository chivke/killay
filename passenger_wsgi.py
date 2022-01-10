import os
import sys


def get_application():
	virtual_env_directory = "env"
	virtual_env = os.path.join(
		os.path.dirname(__file__), virtual_env_directory, 'bin', 'python'
	)
	print(virtual_env)
	if sys.executable != virtual_env:
		os.execl(virtual_env, virtual_env, *sys.argv)
	sys.path.insert(0, os.path.join(os.getcwd(), virtual_env, 'bin'))

	from config import wsgi

	return wsgi.application

application = get_application()
