
import json
import os
import sys
import csv
from datetime import datetime 
import imp
import inspect
from inspect import isclass

from mpiguidelines import machine_setup 

def create_local_dir(dirpath):
    if not os.path.exists(dirpath):
        print ("Creating local experiment directory %s" % dirpath)
        os.system("mkdir -p %s" % dirpath)
    else:
        if os.path.isdir(dirpath):   
            print ("Warning: Local directory already exists - %s" % dirpath)
            return False
    return True
  
def read_json_config_file(filepath):
    try:
        json_data = open(filepath)
        data = json.load(json_data)
    except IOError:
        data = {}
    return data

def write_json_config_file(filepath, data):
    try:
        if os.path.exists(filepath): 
            print ("Warning: Overwriting file - %s" % filepath)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    except:
        print >> sys.stderr, "Cannot write data to file: %s" % filepath
        sys.exit(1)
  
def write_guidelines_to_dataframe(filepath, data, header = None):
    try:
        with open(filepath, "w") as f:
            if header:
                f.write("%s\n" % header)
            for key in data.keys():
                f.write("%s %s\n" % (key, " ".join(data[key])))
    except:
        print >> sys.stderr, "Cannot write data to file: %s" % filepath
        sys.exit(1)


def get_current_time_str():
    return datetime.strftime(datetime.now(), "%Y-%m-%d-%H%M")

def create_exp_name(expid):
    fullname = "%s-%s" % (str(expid), get_current_time_str() )
    return fullname 
  
 
 
 
def read_cvs_file(filepath, fieldnames = None):
    data = []
    file_field_names = {}
    try:
        with open(filepath) as csvfile:
            reader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile), 
                                    fieldnames = fieldnames, delimiter = " ")            
            for row in reader:
                if len(file_field_names) == 0 :
                    file_field_names = row
                    continue
                data.append(row)
                
    except IOError:
        data = []

    assert(len(data) > 0), "Cannot read file or file not correctly formatted (%s)" % (filepath)
    return data




def instantiate_class_from_file(class_path, parent_class):
    # load machine setup class from specified file    
    mach_conf_module = imp.load_source("machconf", class_path)   
    mach_class_list = []
    for name, cls in mach_conf_module.__dict__.items():
        if isclass(cls) and issubclass(cls, parent_class) and not issubclass(parent_class, cls):
            mach_class_list.append(cls)
    
    if len(mach_class_list) == 0:
        print >> sys.stderr, "Cannot load configuration class from: %s" % class_path
        sys.exit(1)
    
    if len(mach_class_list) > 1:
        print >> sys.stderr, "Multiple configuration classes found in: %s" % class_path
        sys.exit(1)    
    
    # instantiate machine setup  class
    try:
        machine_configurator = mach_class_list[0]()
    except Exception, err:
        print 'ERROR: Cannot instantiate class defined in %s: \n' % class_path, str(err)
        exit(1)

    return machine_configurator
    
    


