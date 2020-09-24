###########################################################################
#                                Cliente XMPP                             #
###########################################################################

# @author: Esteban Cabrera Arevalo
# @carnet: 17781

from Register import *
from Client import *


import sys
import time
import logging
import getpass
from optparse import OptionParser

from headers import *

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')


    #Constantes
    server = '@redes2020.xyz'

    #Variables de control
    logged_in = False
    close = False

    default_menu = '''\n
    1. Login.
    2. Registrarse.
    3. Salir'''

    logged_menu = '''\n
    1.
    2.
    3.
    4.
    5.
    6.'''

    print(header)
    while not (close):
        if not logged_in:
            print (default_menu)

            opcion = input("Seleccione una opcion: ")

            if (opcion == "1"):
                print(login)

                username = input("Usuario: ")

                opts.jid = username + server
                opts.password = getpass.getpass("Password: ")

                xmpp = Client(opts.jid, opts.password)
                xmpp.register_plugin('xep_0077')
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Multi-user chat
                xmpp.register_plugin('xep_0096')
                xmpp.register_plugin('xep_0065')
                xmpp.register_plugin('xep_0004')
                if xmpp.connect():
                    xmpp.process()
                    time.sleep(5)
                    logged_in = True
                    print("Bienvenido/a ", username)
                else:
                    print("error")
                    
            elif (opcion == "2"):
                print(register)

                username = input("Usuario: ")

                opts.jid = username + server
                opts.password = getpass.getpass("Password: ")

                xmpp = Register(opts.jid, opts.password)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0004') # Data forms
                xmpp.register_plugin('xep_0066') # Out-of-band Data
                xmpp.register_plugin('xep_0077') # In-band Registration
                if xmpp.connect():
                    xmpp.process(block=True)
                    print("Done")
                else:
                    print("Unable to connect.")

            elif (opcion == "3"):
                close = True
            else:
                print("La opcion que ingreso no existe.")

        else:
            print(menu)

            print (logged_menu)

            opcion = input("Seleccione una opcion: ")