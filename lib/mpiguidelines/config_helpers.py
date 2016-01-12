
import json
import os
import sys
from datetime import datetime
from mpiguidelines.benchmark import benchmarks as bench

def generate_exp_file(expconf, machineconf, exp_dir, local_exec = False):

    config_data = {}
    config_data["exp_info"] = read_json_config_file(expconf)
    config_data["mach_info"] = read_json_config_file(machineconf)
    config_data["exp_name"] = os.path.basename(exp_dir)
    config_data["exp_info"]["exp_base_dir"] = os.path.dirname(exp_dir)
    config_data = translate_and_set_guideline_names(config_data)
    
    if local_exec:
        config_data["mach_info"]["remote_base_dir"] = config_data["exp_info"]["exp_base_dir"]
    
    outdir = exp_dir
    ret = create_local_dir(outdir)
    if not ret:
        print ("Specify another experiment name or path to create a new experiment.\n")
        sys.exit(1)        
    
    config_file_path = os.path.join(outdir, config_data["exp_name"] + ".json")
    write_json_config_file(config_file_path, config_data)
    
    return config_file_path




def translate_and_set_guideline_names(config_data):
    
    #config_data = helpers.read_json_config_file(config_file)
    bench_info = config_data["mach_info"]["benchmark"]
    benchmark = bench.BENCHMARKS[bench_info["type"]](bench_info)

    guidelines = config_data["exp_info"]["guidelines"]
    for gkey in guidelines.keys():
        guideline = guidelines[gkey]
        calls = []
        for (_, g) in enumerate(guideline):
            calls.append(g["mpicall"])
        translated_calls = benchmark.translate_guideline(calls)
        
        # use the MPI call names as they were defined, if no benchmark-specific calls exist
        if not translated_calls:
            translated_calls = calls
        
        for i in xrange(0,len(calls)):    
            guideline[i]["bench_mpicall"] = translated_calls[i]
        guidelines[gkey] = guideline
    config_data["exp_info"]["guidelines"] = guidelines
    
    return config_data      


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
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    except:
        print >> sys.stderr, "Cannot write data to file: %d" % filepath
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
  
 
 
 
