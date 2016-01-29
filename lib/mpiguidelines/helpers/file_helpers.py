
import json
import os
import sys
import csv
from datetime import datetime 


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
  
def write_to_dataframe(filepath, data):
    try:
        with open(filepath, "w") as f:
            f.write("guideline f1 f2\n")
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

    assert(len(data) > 0), "Cannot read prediction results (%s) or file not correctly formatted" % (filepath)
    return data


def get_execution_dir(config_data):    
    if config_data["exp_info"]["local_exec"]:
        execution_dir = os.path.join(config_data["exp_info"]["exp_base_dir"], config_data["exp_name"])
    else:
        execution_dir = config_data["mach_info"]["remote_base_dir"]
    return execution_dir


