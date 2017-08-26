import os
import logging as log
from CfgParser import CfgParser

def readConfig():
  config = CfgParser()
  filename = os.environ['GDAX_CFG'] + "/" + "common.cfg"
  config.readFiles([filename])
  print("reading " + filename)
  print(config.getConfig(['File_Path','File_Name']))
  return config.getConfig(['File_Path','File_Name'])

def writeFile(data,filename):
  try:
    filename = os.environ['GDAX_DATA'] + '/' + filename
    log.info('Writing data to file=' + filename)
    with open(filename) as f:
      for line in data:
        f.write(line)
    log.info('Finished writing to file')
  except Exception as e:
    log.error(str(e))
