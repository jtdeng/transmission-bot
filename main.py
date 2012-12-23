#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
from settings import logger
from xmppbot import TransmissionBot
from timer import PeriodicTimer
import tasks  
import traceback

if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.
    xmpp = TransmissionBot(settings.xmpp_username, settings.xmpp_password)
    
    if settings.use_proxy:
        xmpp.use_proxy = True
        xmpp.proxy_config = settings.proxy_config
    
    try:
        xmpp.connect()
        task = PeriodicTimer(settings.task_interval, tasks.periodic_task, xmpp, settings)
        task.start()
        xmpp.process(block=True)
        print 'xmpp process finished'
        task.cancel()
    except:
        logger.fatal(traceback.format_exc())
