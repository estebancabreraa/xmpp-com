###########################################################################
#                                Cliente XMPP                             #
###########################################################################

# @author: Esteban Cabrera Arevalo
# @carnet: 17781

import Register
import Chat

import sys
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


    #Variables de control
    logged_in = False
    close = False

    default_menu = '''\n
    1. Login.
    2. Registrarse.
    3. Salir'''

    print(header)
    while not (close):
        if not logged_in:
            print (default_menu)

            opcion = input("Seleccione una opcion: ")

            if (opcion == "1"):
                print(login)

                username = input("Usuario: ")
                password = input("Contraseña: ")
            elif (opcion == "2"):
                print(register)
            elif (opcion == "3"):
                close = True
            else:
                print("La opcion que ingreso no existe.")
