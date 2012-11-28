#!/usr/bin/env python
# -*- coding: utf-8 -*-

# implementation for a XMPP bot

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import traceback
import settings
from settings import logger

import commands


class TransmissionBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        #register plugins
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0047', {'accept_stream': self.accept_stream}) # In-band Bytestreams

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("ibb_stream_start", self.stream_start)
        self.add_event_handler("ibb_stream_data", self.stream_data)


    def session_start(self, event):
        try:
            self.send_presence()
            self.get_roster()
        except IqError as err:
            logger.error('There was an error getting the roster')
            logger.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            logger.error('Server is taking too long to respond')
            self.disconnect()

    def message(self, msg):
        if msg['type'] not in ('chat', 'normal'):
            logger.debug('Strange message type: %(type)s' % msg)
            return
        #logger.info('Message from %(from)s: %(body)s' % msg)
        
        msg_text = msg['body'].strip()
        # msg['from'] is a JID object
        # http://sleekxmpp.com/api/xmlstream/jid.html
        from_user = msg['from'].bare 
        logger.info('FROM:' + from_user)
        logger.info('MSG:' + msg_text)

        try:
            if (from_user in settings.accept_command_from) and msg_text.startswith("$"):
                resp = commands.execute(msg_text[1:])
                msg.reply('\n'+resp).send()
            else:
                msg.reply(msg_text).send()
        except Exception,e:
            exc = traceback.format_exc()
            msg.reply(exc).send()

    # def changed_status(self, ):
    #     pass

    # def disconnected(self,):
    #     pass

    def accept_stream(self, iq):
        """
        Check that it is ok to accept a stream request. 

        Controlling stream acceptance can be done via either:
            - setting 'auto_accept' to False in the plugin
              configuration. The default is True.
            - setting 'accept_stream' to a function which accepts
              an Iq stanza as its argument, like this one.

        The accept_stream function will be used if it exists, and the
        auto_accept value will be used otherwise.
        """
        return True

    def stream_start(self, stream):
        #print('Stream opened: %s from %s' % (stream.sid, stream.receiver))
        pass

    def stream_data(self, event):
        #print(event['data'])
        pass

