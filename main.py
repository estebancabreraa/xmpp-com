###########################################################################
#                                Cliente XMPP                             #
###########################################################################

# @author: Esteban Cabrera Arevalo
# @carnet: 17781

from Register import *
from Client import *


import sys
import time #
import logging #
import getpass
from optparse import OptionParser
from tabulate import tabulate #

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
    chat_format = "@conference.redes2020.xyz"

    #Variables de control
    logged_in = False
    close = False

    default_menu = '''\n
    1. Login.
    2. Registrarse.
    3. Salir'''

    logged_menu = '''\n
    1. Mostrar usuarios existentes.
    2. Ver datos de un usuario.
    3. Agregar un nuevo contacto.
    4. Mostrar contactos.
    5. Enviar un mensaje.
    6. Mostrar las salas de chat.
    7. Crear una sala de chat.
    8. Mensaje a una sala.
    10. Cerrar sesion.
    11. Salir.
    '''

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

                client = Client(opts.jid, opts.password)
                client.register_plugin('xep_0077')
                client.register_plugin('xep_0030') # Service Discovery
                client.register_plugin('xep_0199') # XMPP Ping
                client.register_plugin('xep_0045') # Multi-user chat
                client.register_plugin('xep_0096')
                client.register_plugin('xep_0065')
                client.register_plugin('xep_0004')
                if client.connect():
                    client.process()
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

                client = Register(opts.jid, opts.password)
                client.register_plugin('xep_0030') # Service Discovery
                client.register_plugin('xep_0004') # Data forms
                client.register_plugin('xep_0066') # Out-of-band Data
                client.register_plugin('xep_0077') # In-band Registration
                if client.connect():
                    client.process(block=True)
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

            if (opcion == "1"):
                print(users)
                users = client.show_Users()
                users_table_list = tabulate(users, headers=['Email', 'JID', 'Username', 'Name'], tablefmt='grid')
                print(users_table_list)
            if (opcion == "2"):
                print(users)
                jid = input('Ingrese el nombre de usuario: ')
                user = client.show_user(jid)
                data = tabulate(user, headers=['JID', 'Username',  'Name', 'Email'], tablefmt='grid')
                print(data)
            if (opcion == "3"):
                jid = input("Ingrese el JID del usuario a agregar: ")
                client.add_contact(jid)
                print("Se ha añadido el contacto exitosamente!")
                client.show_contacts()    
            if (opcion == "4"):
                print(users)
                client.show_contacts()
            if (opcion == "5"):
                print(message)
                
                to = input("Para: ")
                msg = input("Mensaje: ")

                print("1. Enviar.")
                print("2. Cancelar.")

                opcion = input("Ingrese una opcion: ")

                if (opcion == "1"):
                    to = to + server
                    
                    client.snd_message(msg, to)
                    print("Mensaje enviado exitosamente!")
                elif (opcion == "2"):
                    print("Se cancelo el envio del mensaje.")
                else:
                    print("No existe esta opcion.")

            if (opcion == "6"):
                print(chatrooms)

                client.show_chatRooms()
            
            if (opcion == "7"):
                print(chatrooms)
                
                chat_room = input("Ingrese el JID de la sala para crear: ")
                chat_room = chat_room + chat_format
                nick = input("Ingrese su apodo: ")

                client.create_chatRroom(chat_room, nick)
                
                print("Sala creada. Te has unido a la sala indicada!")
            if (opcion == "8"):
                print(chatrooms)
                chat_format = "@conference.redes2020.xyz"

                chat_room = input("Ingrese el nombre de la sala para unirse: ")
                chat_room = chat_room + chat_format
                nick = input("Ingrese su apodo: ")

                client.join_chatRoom(chat_room, nick)
                
                print("Te has unido a la sala indicada!")
            if (opcion == "10"):
                client.logout()
                logged_in = False
                print(goodbye)
                print(menu)
            if (opcion == "11"):
                client.logout()
                logged_in = False
                close = True
                print(goodbye)
 

