#!/home/ubuntu/anaconda3/bin/python

import json
import time
from websocket import create_connection
import logging as log
import Helper as helper
from PyLogger import PyLogger

class WebSocketClient(object):

  def __init__(self,config):
    self.config = config
    self.feed = "wss://ws-feed.gdax.com"
    self.productList = ["BTC-USD"]
    self.data = []

  def subscribe(self):
    try:
      self.ws = create_connection(self.feed)
      self.ws.send(json.dumps({
        "type": "subscribe",
        "product_ids": self.productList
      }))
      log.info("Successfully subscribed to market data feed")
    except Exception as e:
      log.error(str(e))

  def receiveData(self,period=0):
    try:
      start = time.time()
      while True:
        result = self.ws.recv()
        result = json.loads(result)
#        print ("Received '%s'" % result)
        self.data.append(result)
        if period:
          if time.time() > (start + period):
            print("Stopping after " + str(period) + "seconds")
            return
    except Exception as e:
      log.error(str(e))

  def stop(self):
    try:
      self.ws.close()
    except Exception as e:
      log.error(str(e))

  def writeData(self):
    try:
      helper.writeFile(self.data,self.config['File_Name']['datafile'])
    except Exception as e:
      log.error(str(e))

def main():
  """
  Main to exemplify usage
  """

  config = helper.readConfig()

  PyLogger(config['File_Path']['log'] + config['File_Name']['logfile'])
  client = WebSocketClient(config)
  client.subscribe()
  client.receiveData(1)
  client.stop()
  client.writeData()

if __name__=='__main__':
  main()  
