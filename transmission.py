#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import transmissionrpc

TransmissionClient = transmissionrpc.Client(**settings.transmission_rpc_config)	
