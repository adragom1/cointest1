import configparser
import re
import os
import sys
import logging as log
from copy import deepcopy

class CfgParser(object):
  """
  This class implements additional functionality to the default ConfigParser
  $(XXX)      - code variable
  $[X:Y]      - cross section reference, Section X: Value Y
  ${XXX}      - environment variable
  include=XXX - read config from additional files 
  """

  def __init__(self):
    self.config       = configparser.ConfigParser()
    self.path         = os.environ['GDAX_CFG']
    self.sections     = []
    self.finalConfig  = {}
    self.includeFiles = {}
	
  def readFileIncludes(self,files):
    """
    This method creates the file order list
    """
	
    try:
      for file in files:
        for section in self.config.sections():
          self.config.remove_section()
        self.sections = []
        self.config.read(self.path + file)
        for section in self.config.sections():
          if section not in self.sections:
            self.sections.append(section)	  
	
        #Find files to be included
        includes = self.findIncludes()
        #Remove duplicates
        if includes and not set(includes.values()).issubset(self.includeFiles.values()):
          for section,file in includes.iteritems():
            includes.pop(section,'None')
	  #Prepend file to read list
          for section,file in deepcopy(includes).iteritems():
            if section in self.includeFiles:
              self.includeFiles[section][:0] = file
            else:
              self.includeFiles[section] = file
            includes.pop(section)
          if includes.values:
            self.readFileIncludes(include.values())
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      log.error(str(e))

  def readFiles(self,files):
    try:
      self.readFileIncludes(files)
      files[:0] = self.includeFiles.values()
      self.finalConfig = {}
      for file in files:
        for section in self.config.sections():
          self.config.remove_section(section)
        self.sections = []
        self.config.read(self.path + file)
        for section in self.config.sections():
          if section not in self.sections:
            self.sections.append(section)
          if section in self.finalConfig:
            sectionMap = self.configSectionMap(section)
            for key in sectionMap:
              if key not in self.finalConfig[section]:
                self.finalConfig[section][key] = sectionMap[key]
          else:
            self.finalConfig[section] = self.configSectionMap(section)
          self.applyInterpolation()	
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      log.error(str(e))	
		
  def getSections(self):
    return self.sections
	
  def configSectionMap(self,section):
    """
    Reads all variables within a section
    """
	
    try:
      dict1 = {}
      options = self.config.options(section)
      for option in options:
        try:
          dict1[option] = self.config.get(section,option)
          if dict1[option] == -1:
            DebugPrint("skip: %s" % option)
        except:
          log.error()
          dict1[option] = None
      return dict1
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      log.error(str(e))	

  def logConfig(self):
    for k,v in self.finalConfig.iteritems:
      log.info(k + "=" + v)

  def replaceEnv(self,value):
    """
    Replace environment variables
    """
	
    try:
      while '${' in value:
        occurence = re.search('\$\{(.+?)\}',value).group(1)
        value = value.replace('${' + occurence + '}', os.environ[occurence])
      return value		
    except Exception as e:
      log.error(str(e))
 
  def replaceCSR(self,value):
    """
    Replace cross-section references
    """
	
    try:
      while '$[' in value:
        occurence = re.search('\$\[(.+?)\]',value).group(1)
        sect,var = occurence.split(':')
        if var.lower() in self.finalConfig[sect]:
          value = value.replace('$[' + occurence + ']',self.finalConfig[sect][var.lower()])
        else:
          value = value.replace('$[' + occurence + ']' + ' Not Found')
          log.info('Could not find reference to section=' + sect + ', var=' + var.lower())
      return value
    except Exception as e:
      log.error(str(e))

  def getConfig(self,sections):
    """
    Reades sections within config file
    """
	
    try:
      requiredSections = {}
      for section in sections:
        if section in self.finalConfig:
          requiredSections[section] = self.finalConfig[section]
        else:
          log.info('Could not find section=' + section)
      return requiredSections
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      log.error(str(e))

  def applyInterpolation(self):
    """
    Apply interpolation - variable replacement
    """
	
    try:
      for section,variable in self.finalConfig.items():
        for key,value in variable.items():
          if '$' in value:
            value = self.replaceEnv(value)
            value = self.replaceCSR(value)
            variable[key] = value
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      log.error(str(e))
	  
  def findIncludes(self):
    try:
      includeFiles = {}
      for section in self.sections:
        sectionMap = self.configSectionMap(section)
        if 'include' in sectionMap:
          val = sectionMap['include']
          if '$' in val:
            val = self.replaceEnv(val)
            val = self.replaceCSR(val)
            includeFiles[section] = val.lower()  
      return includeFiles
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      log.error(str(e))

def main():
  """
  Main to exemplify usage
  """
  
  config = CfgParser()
  config.readFiles(['common.cfg','specific.cfg'])
  for k,v in config.getConfig(['Section1','Section2']).iteritems():
    log.info(k + '=' + v)
	
if __name__=='__main__':
  main()  
