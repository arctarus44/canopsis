
from time import time


def monitoringdeco(function):

	def monitor(*args, **kwargs):

		now = time()

		result = function(*args, **kwargs)

		elaspedtime = time() - now

		#... do something with the function result or now

		return result

	return monitor



def event_processing(event, **kwargs):
	"""something to do ...."""

	pass