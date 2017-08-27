import os
import logging as log
from CfgParser import CfgParser

def readConfig():
  config = CfgParser()
  filename = "common.cfg"
  config.readFiles([filename])
  return config.getConfig(['File_Path','File_Name'])

def writeFile(data,filename):
  try:
    filename = os.environ['GDAX_DATA'] + '/' + filename
    log.info('Writing data to file=' + filename)
    f = open(filename,'w')
    print(data)
    for line in data:
      f.write(str(line))
    f.close()
    log.info('Finished writing to file')
  except Exception as e:
    log.error(str(e))
