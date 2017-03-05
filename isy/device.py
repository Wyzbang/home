#!/usr/bin/env python
"""
ISY99i Device
"""

class Device(object):
    
    def __init__(self, name, address):
        """
        Args:
            name = display name for Insteon Device
            address = Insteon id for the device (XX YY ZZ A)
        """
        self.address = address
        self.name = name

