import logging
import os
import time

class PyLogger(object):

#  def __init__(self,filename):
#    self.logger    = logging.getLogger('PyLogger')
#    self.format    = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
#    self.handler   = logging.FileHandler(filename)
#    self.formatter = logging.Formatter(self.format) 
#    self.handler.setLevel(os.environ["LOGLEVEL"])
#    self.handler.setFormatter(self.formatter)
#    self.logger.addHandler(self.handler)
  
  def __init__(self,filename):
    filename = filename + "." + str(time.time())
    logging.basicConfig(format="[%(filename)s:%(lineno)s - %(funcName)20s() ]%(asctime)s: %(message)s",
                        level=os.environ["LOGLEVEL"],
                        filename=filename)
