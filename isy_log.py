#!/usr/bin/env python
"""
"""
import datetime
import logging
import os

from isy.server import IsyServer
from isy.log import STATUS, ON, OFF

logging.basicConfig(level=logging.DEBUG)
TODAY = datetime.date.today().strftime("%Y%m%d")

class isyReport(object):
    
    def __init__(self, address, path):
        """
        :param address: isy server ip
        :param path: output path for logs
        """
        self.isy = IsyServer(address)

        today = datetime.datetime.now()
        folder = today.strftime("%Y%m%d")
        self.path = path + os.sep + folder

        self.nodes = {}
        

    def writeCSV(self, node, items):

        try:
            os.makedirs(self.path)
        except OSError:
            pass

        out = open("%s%s%s_%s.csv" % (self.path, os.sep, node, TODAY), 'w')
        out.write("on,off,duration\n")
    
        for item in items:
            on = item['on']
            off = item['off']
            try:
                duration = (off - on).total_seconds()
            except:
                duration = -1
                    
            string = "%s,%s,%d\n" % ( on, off, duration )  
            out.write( string )
                
        out.close()


    def setON(self, name, timestamp):
        self.nodes[name].append( { 'on':timestamp, 'off':None } )

    
    def setOFF(self, name, timestamp):
        # If there is not an previous on record, add a new line
        if( len(self.nodes[name]) == 0 or self.nodes[name][-1]['off'] != None ):
            self.nodes[name].append( { 'on':None } )
                        
        self.nodes[name][-1]['off'] = timestamp


    def fullReport(self):
        addrs, names = self.isy.getNodes()
    
        for item in self.isy.getLog():
            
            name = names.get(item.node, item.node).replace(" ", "-").replace(":", "")
            
            if name not in self.nodes:
                self.nodes[name] = []
            
            if item.control == STATUS:
                if item.action != 0:  # on
                    self.setON( name, item.timestamp )
                else:
                    self.setOFF( name, item.timestamp )
                    
            elif item.control == ON:
                self.setON( name, item.timestamp )

            elif item.control == OFF:
                self.setOFF(name, item.timestamp)
                    
        
        for node, items in self.nodes.items():
            logging.info("**** NODE: %s (%d)" % (node, len(items)))
            if len(items) > 0:
                self.writeCSV(node, items)
    

if __name__ == "__main__":
    r = isyReport("192.168.1.111", "d:\\src\\home\\logs")
    r.fullReport()

