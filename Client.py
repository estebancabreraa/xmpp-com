import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File

class Client(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = ''
        self.nick = ''

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.incoming_message)
        self.add_event_handler("changed_status", self.notification_changed_status)
        self.add_event_handler("changed_subscription", self.notification_changed_subscription) 
        self.add_event_handler("got_offline", self.notification_got_offline)
        self.add_event_handler("got_online", self.notification_got_online)


    def start(self, event):
        print("running start")
        self.get_roster()
        self.send_presence()
    
    def notification_changed_status(self, presence):
        print("Notificaction Changed Status")
        print(presence['status'])

    def notification_changed_subscription(self, presence):
        print("Notificaction Changed Subscription")
        print(presence['type'])

    def notification_got_offline(self, presence):
        print("Notificaction Presence Offline")
        print(presence['type'])

    def notification_got_online(self, presence):
        print("Notificaction Presence Online")
        print(presence['type'])

    def incoming_message(self, message):
        if message['type'] in ('chat','normal'):
            print('Direct Message')
            print(message['from'], message['body'])

    def logout(self):
        self.disconnect(wait=True)

    def message(self, msg, recipient):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=recipient,
                          mbody=msg,
                          mtype='chat')
    
    def status(self, status):
        self.send_presence()
        self.get_roster()
        self.make_presence(pfrom=self.jid, pstatus=status)

    def send_subscription(self, recipient):
        self.send_presence_subscription(pto=recipient, ptype='subscribe')

    def show_contacts(self):
        self.send_presence()
        self.get_roster()
        self.client_roster
        print("Contactos: ", self.client_roster.groups())

    def remove_contact(self, jid):
        self.send_presence()
        self.get_roster()
        self.del_roster_item(jid)

    def join_room(self, room, nick):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(room,
                                        nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)
        self.add_event_handler("groupchat_message", self.muc_message)

    def create_room(self, room, nick):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(room,
                                        nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)
        roomform = self.plugin['xep_0045'].getRoomConfig(room)
        roomform.set_values({
            'muc#roomconfig_persistentroom': 1,
            'muc#roomconfig_roomdesc': 'Plin plin plon'
        })
        self.plugin['xep_0045'].configureRoom(room, form=roomform)
    
    def group_message(self, msg):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.room,
                          mbody=msg,
                          mtype='groupchat')

    def get_chatRooms(self):
        self.send_presence()
        self.get_roster()
        result = self.plugin['xep_0030'].get_items(jid='conference.redes2020.xyz')
        for room in result['disco_items']:
            print(room['jid'])

    def muc_message(self, msg):
        print("muc message")
        if msg['mucnick'] != self.nick:
            print(msg['mucroom'])
            print(msg['mucnick'], ': ',msg['body'])
    
    def show_Users(self):
        iq_stanza = self.Iq()
        iq_stanza['type'] = 'set'
        iq_stanza['id'] = 'search_result'
        iq_stanza['to'] = 'search.redes2020.xyz'
        iq_stanza['from'] = self.boundjid.bare
        que = ET.fromstring("<query xmlns='jabber:iq:search'> \
                                <x xmlns='jabber:x:data' type='submit'> \
                                    <field type='hidden' var='FORM_TYPE'> \
                                        <value>jabber:iq:search</value> \
                                    </field> \
                                    <field var='Username'> \
                                        <value>1</value> \
                                    </field> \
                                    <field var='search'> \
                                        <value>*</value> \
                                    </field> \
                                </x> \
                              </query>")
        iq_stanza.append(que)
        try:
            users = iq_stanza.send()
            cont = 0
            data= []
            users_info = []
            for i in users.findall('.//{jabber:x:data}value'):
                cont += 1
                user_data = ''
                if i.text != None:
                    user_data = i.text
                data.append(user_data)
                if cont == 4:
                    cont = 0
                    users_info.append(data)
                    data=[]
            return users_info
        except IqError as err:
            print('No se pueden mostrar: %s' % err)
        except IqTimeout:
            print('No se recibe respeusta del servidor')
