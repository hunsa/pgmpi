#    PGMPI - Performance Guideline Verification Tool for MPI Collectives
#
#    Copyright 2016 Alexandra Carpen-Amarie, Sascha Hunold
#    Research Group for Parallel Computing
#    Faculty of Informatics
#    Vienna University of Technology, Austria
# 
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import json
import os
import sys
import csv
from datetime import datetime 
import imp
import inspect
from inspect import isclass

def create_local_dir(dirpath):
    print ("Creating local experiment directory %s" % dirpath)
    if not os.path.exists(dirpath):
        os.system("mkdir -p %s" % dirpath)
    else:
        if not os.path.isdir(dirpath):   
            print  >> sys.stderr, "ERROR: Cannot create directory, a file with the same name already exists: %s" % dirpath
            exit(1)
    return True
  
def read_json_config_file(filepath):
    try:
        json_data = open(filepath)
        data = json.load(json_data)
    except IOError:
        data = {}
        print >> sys.stderr, "Cannot read data from file: %s" % filepath
        sys.exit(1)
    return data

def write_json_config_file(filepath, data):
    try:
        if os.path.exists(filepath): 
            print  >> sys.stderr, "Warning: Overwriting file - %s" % filepath
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
        print >> sys.stderr, "Cannot read data from file: %s" % filepath
        sys.exit(1)

    assert(len(data) > 0), "Cannot read file or file not correctly formatted (%s)" % (filepath)
    return data




def get_class_from_file(class_path, parent_class):
    # load machine setup class from specified file    
    conf_module = imp.load_source("mymodule", class_path)   
    class_list = []
    for name, cls in conf_module.__dict__.items():
        if isclass(cls) and issubclass(cls, parent_class) and not issubclass(parent_class, cls):
            class_list.append(cls)
    
    if len(class_list) == 0:
        print >> sys.stderr, "Cannot load configuration class from: %s" % class_path
        sys.exit(1)
    
    if len(class_list) > 1:
        print >> sys.stderr, "Multiple configuration classes found in: %s" % class_path
        sys.exit(1)    
    
    # instantiate machine setup  class
    try:
        myclass = class_list[0]
    except Exception, err:
        print  >> sys.stderr, 'ERROR: Cannot instantiate class defined in %s: \n' % class_path, str(err)
        exit(1)

    return myclass
    
    


