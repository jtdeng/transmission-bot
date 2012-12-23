#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this module wraps the transmission RPC client

import settings
import transmissionrpc

TransmissionClient = transmissionrpc.Client(**settings.transmission_rpc_config)	
