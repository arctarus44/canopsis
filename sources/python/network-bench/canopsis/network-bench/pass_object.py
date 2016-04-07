# coding: utf-8

class Object_pass(object):

    def __init__(self, object, time, *args, **kwargs):
        super(Object_pass, self).__init__(*args, **kwargs)
        self.object = object
        self.time = time

    def get_object(self):
        return self.object

    def get_time(self):
        return self.time
