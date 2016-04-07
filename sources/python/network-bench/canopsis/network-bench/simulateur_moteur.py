# coding: utf-8
from __future__ import unicode_literals
import zmq
import time
from collections import Hashable
import pass_object

class Simulateur(object):

    def __init__(self, *args, **kwargs):
        super(Simulateur, self).__init__(*args, **kwargs)
        context = zmq.Context()
        self.zmq_socket = context.socket(zmq.PUSH)
        self.zmq_socket.connect("tcp://127.0.0.1:4242")

    def send(self, message):
        print('envoi')
        list = []
        list.append(message)
        list.append(time.time())
        self.zmq_socket.send_pyobj(list)
        print('gone')
        #envoi du message normal via rabbitmq

    def receive(self, message):
        """fonction de test de recevage normalement sans parametre message
        le message etant ce qu'on reçoit normalement"""
        self.zmq_socket.send_pyobj((message, time.time()))
        #reception du vrai message de la vrai vi du moteur normale et véritable

