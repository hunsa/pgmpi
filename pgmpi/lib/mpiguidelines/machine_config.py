
import os
import sys

    
def get_mpi_call(nodes, nnp, mach_info):
    call = ""

    machinefile = ""
    try: 
        machinefile = "-machinefile %s" % mach_info["machinefile"]
    except:
        pass  

    if mach_info["mpiimpl"] == "nec":             # NEC calls to mpirun
        # remove pinning option if not required
        pin_option = "-pin_mode consec"
        if mach_info["pinning"] == "nopin":
            pin_option = ""
        if mach_info["pinning"] == "pinrev":
            pin_option = "-pin_mode consec_rev"
        call = "%s/mpirun -node 1-%s -nnp %s %s" % ( mach_info["mpi_path"], nodes, nnp, pin_option )
    
    
    elif mach_info["mpiimpl"] == "mvapich":       # MVAPICH calls to mpirun
        np = nodes * nnp
        
        # remove pinning option if not required
        pin_option = "-bind-to rr"
        if mach_info["pinning"] == "nopin":
            pin_option = ""

        call = "%s/mpirun -np %d -ppn %s %s %s" \
            % ( mach_info["mpi_path"], np, nnp, pin_option, machinefile)

    elif mach_info["mpiimpl"] == "mpich":      
        np = nodes * nnp
        
        # remove pinning option if not required
        pin_option = "-bind-to rr"
        if mach_info["pinning"] == "nopin":
            pin_option = ""

        call = "%s/mpirun -np %d -ppn %s %s %s" \
            % ( mach_info["mpi_path"], np, nnp, pin_option, machinefile)
            
    elif mach_info["mpiimpl"] == "openmpi":      
        np = nodes * nnp
        #/opt/openmpi-1.10.1/bin/mpirun -np 32 -bind-to core -npernode 16 -machinefile machinefile 
        
        # remove pinning option if not required
        pin_option = "-bind-to core"
        if mach_info["pinning"] == "nopin":
            pin_option = ""

        call = "%s/mpirun -np %d -npernode %s %s %s" \
            % ( mach_info["mpi_path"], np, nnp, pin_option, machinefile)
            
    elif mach_info["mpiimpl"] == "intelmpi":      
        np = nodes * nnp
        
        # remove pinning option if not required
        pin_option = "-bind-to core"
        if mach_info["pinning"] == "nopin":
            pin_option = ""

        call = "mpirun -np %d -ppn %s %s %s" \
            % ( np, nnp, pin_option, machinefile)

    return call



def get_jobfile_header(nodes, nnp, mach_info, remote_output_dir):
    
    header = ""
    try:
        name = mach_info["mach_name"]
        
        if name == "vsc3":
            
            qos_name = ""
            try: 
                qos_name = "#SBATCH --qos=%s" % mach_info["qos_name"]
            except:
                pass  

            part_name = ""
            try: 
                part_name = "#SBATCH --partition=%s" % mach_info["partition_name"]
            except:
                pass                  
            
            input_dir = os.path.join(remote_output_dir, "mpicfg")
            machinefile = "nodesfile"
            
            header = """#!/bin/sh
#SBATCH -J mpibench
#SBATCH -N %d
#SBATCH --ntasks-per-core=1
%s
%s
export SLURM_CPU_FREQ_REQ="High"

mkdir -p %s
scontrol show hostnames $SLURM_NODELIST  > %s/%s
            
            """ % (nodes, qos_name, part_name, input_dir, input_dir, machinefile)
        
    except: # machine name not defined => no header to return
        pass
        
    
    return header
    
    
    
def get_mpi_call_suffix(mach_info, remote_output_dir):
    
    suffix = ""
    try:
        name = mach_info["mach_name"]
        
        if name == "vsc3":
            input_dir = os.path.join(remote_output_dir, "mpicfg")
            machinefile = "nodesfile" 
            suffix = "-machinefile %s/%s" %(input_dir, machinefile)       
            
    except:
        pass
    
    return suffix
    
    
    
    
    
    


