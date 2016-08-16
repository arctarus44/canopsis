"""from canopsis.schema import edit

path_transfo = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/transformation_dictionary.json'

edit.add(path_transfo, '/test', 'TT')
edit.add(path_transfo, '/info/entity_id', 'bb', 'add1')
edit.replace(path_transfo, '/version', '2.0.0')
edit.remove(path_transfo, '/essai1')"""

from canopsis.schema.migration import core
#from canopsis.middleware.core import Middleware


path_transfo = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/transformation_dictionary.json'

core.migrate(path_transfo)