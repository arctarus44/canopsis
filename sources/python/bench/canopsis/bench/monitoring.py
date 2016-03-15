from time import time

from psutil import Process

from canopsis.middleware.registry import MiddlewareRegistry

from threading import Thread

import os


class Manager(MiddlewareRegistry):

	def monitoring(function, *args, **kwargs):
		def montitor():

			func_thread =  FuncThread(function, *args, **kwargs)
			monito = MonitoThread(func_thread)

			monito.start()
			func_thread.start()

			result = func_thread.get_func_result()

			return result

		return monitor

	def worker(function, *args, **kwargs):
		now = time()
		res = function(*args, **kwargs)
		elapsed = time() - now
		return res


	def monitoring():

class FuncThread(Thread):
	def __init__self(self, func, *args, **kwargs):
		super(FuncThread, self).__init__(*args, **kwargs)
		self.func_result = None
		self.func = func
		self.now = time()
		self.elapsed = 0

	def run(self):
		self.func_result = self.func(
		self.elapsed = time() - now

	def get_func_result():
		return func_result

	def get_elapsed():
		return self.elapsed


class MonitoThread(Thread):
	def __init__(self, functhread):
		super(MonitoThread, self).__init__(*args, **kwargs)
		self.ram_at_beginning = psutil.virtual_memory().used
		self.ram_while_running = 0
		self.ram_used = 0

	def run(self):
		while functhread.isAlive:
			print('true')
			ram_while_running = psutil.virtual_memory().used
		print(dead)
		self.ram_used = ram_while_running - ram_at_beginning

		def get_ram_used():
			return self.ram_used