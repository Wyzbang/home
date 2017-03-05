#!/usr/bin/env python
"""
ISY99i Log Entry
"""
import datetime


# Control Codes
STATUS = "ST"
OFF = "DOF"
ON = "DON"


def logstrip( line ):
    """ Strip extra characters from log line 
    ISY log as (\000) on some lines"""
    
    return line.strip("\000").strip()


def convertISYtoDatetime( isyTime ):
    """ Convert ISY99i log time-stamp to python datetime object"""
    
    # ISY Epoch is 1/1/1900
    isyEpoch = datetime.datetime( 1900, 1, 1, 0, 0, 0 )
    return isyEpoch + datetime.timedelta( seconds=isyTime )


class LogEntry(object):
    
    def __init__( self, node, control, action, timestamp ):
        self.node = node
        self.control = control
        self.action = action
        self.timestamp = timestamp
    
    
    def __str__(self):
        return ( "%s|%s|%s|%s" % (self.node, self.control, self.action, self.timestamp ) )
    
    
    @classmethod
    def parse( cls, entry ):
        
        if( entry != "" ):
            cleaned = logstrip(entry)
            parts = cleaned.split("\t")
        
            # INSTEON Device    Control    Value    Time    User    Log Type
            node = parts[0]
            control = parts[1]
            
            try:
                action = int(parts[2])
            except ValueError:
                action = parts[2]
                
            isyTimeStamp = int(parts[3])
            timestamp  = convertISYtoDatetime(isyTimeStamp)
            
            item = cls(node, control, action, timestamp)
            return item
            
        else:
            return None

