#!/usr/bin/env python
"""
ISY99i Server access via RestAPI
"""
import http.client
import xml.etree.ElementTree

from isy.log import LogEntry 


LOG = "/rest/log"
NODES = "/rest/nodes"
HEADERS = {
    "Accept": "application/xml",
    "Conetnet-Type": "application/xml",
    "Authorization": "Basic YWRtaW46YWRtaW4="
    }


class IsyServer(object):
    
    def __init__( self, address ):
        self.address = address


    def isyCall(self, endpoint):
        conn = http.client.HTTPConnection( self.address )
        conn.request( "GET", endpoint, None, HEADERS )
        res = conn.getresponse()
        if( res.status != 200 ):
            raise Exception( "ISY Device communication failed: %d %s" % (res.status, res.reason) )
        
        b = res.read()
        data = b.decode("utf-8")
        
        return data
        
        
    def getNodes(self):
        """Get list of nodes
        RETURN: Dictionaries of addr:name and name:addr"""
        data = self.isyCall(NODES)
        
        root = xml.etree.ElementTree.fromstring(data)
        addrs = {}
        names = {}
        
        nodes = []
        
        for node in root.iter("node"):
            nodes.append(node)

        for node in root.iter("group"):
            nodes.append(node)

        for node in nodes:
            addr = node.find("address").text
            name = node.find("name").text

            names[addr] = name            
            addrs[name] = addr
        
        return addrs, names
            
        
    def getLog( self ):
        """List of log entries"""
        data = self.isyCall(LOG)
        lines = data.split("\n")
        
        log = []
        for line in lines:
            item = LogEntry.parse(line.strip())
            if item:
                log.append( item )
                
        return log
