from ..core import Patch, registerpatch

from ...lang.json import JsonSchema


@registerpatch(JsonSchema)
class JSONPatch(Patch):

	def process(self, data):

		raise NotImplementedError()
