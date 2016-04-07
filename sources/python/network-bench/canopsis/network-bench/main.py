from network import Serv
from time import sleep
from simulateur_moteur import Simulateur

serv = Serv()
serv.start()

simulateur = Simulateur()

simulateur.send('coucou bonjour')
simulateur.send({'test': 'object'})

sleep(2)

simulateur.receive('coucou bonjour')

sleep(1)

simulateur.receive({'test': 'object'})

serv.stop()
