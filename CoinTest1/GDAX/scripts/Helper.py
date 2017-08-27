import os
import logging as log
import argparse
from CfgParser import CfgParser

def parseArgs():
  try:
    parser = argparse.ArgumentParser(description=
    "This is a WebSocket implementation for a Market Data Client.\
    Please set environment before usage, i.e. '. $GDAX_HOME/env/setenv.sh'.\
    If period is not provided, the client will run until process is stopped/killed.")
    parser.add_argument("-p", "--period", type=int, help="time in seconds the client should run for")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()
    return args
  except Exception as e:
    log.error(str(e))

def readConfig():
  config = CfgParser()
  filename = "common.cfg"
  config.readFiles([filename])
  return config.getConfig(['File_Path','File_Name'])

def writeLines(data,filename):
  with open(filename,'w') as f:
    for line in data:
      f.write(str(line))

def writeToFile(data,filename):
  try:
    filename = os.environ['GDAX_DATA'] + '/' + filename
#    if os.path.exists(filename):
#     writeLines(data,filename)
#    else:
    f = open(filename,'w')
    for line in data:
      f.write(str(line))
    f.close()
  except Exception as e:
    log.error(str(e))
