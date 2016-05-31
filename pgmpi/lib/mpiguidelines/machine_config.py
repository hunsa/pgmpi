
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
    
    header = []
    if "mach_name" in mach_info:     
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
            
            header = header + ["#!/bin/sh",
                               "#SBATCH -J mpibench",
                               "#SBATCH -N %d"   % nodes,
                               "#SBATCH --ntasks-per-core=1",
                               qos_name,
                               part_name,
                               "export SLURM_CPU_FREQ_REQ=\"High\"",
                               "mkdir -p %s" % input_dir,
                               "scontrol show hostnames $SLURM_NODELIST  > %s/%s" % (input_dir, machinefile)
                               ]
    
    header = header + ["if [ ! -e %s ]; then " % mach_info["mpi_path"], 
                       "echo \"MPI library path is incorrect: %s \" " % mach_info["mpi_path"],
                       "exit 1",
                       "fi"
                       ]
    
    if "machinefile" in mach_info:      # if the machinefile is defined
        header = header + ["if [ ! -f %s ]; then " % mach_info["machinefile"], 
                           "echo \"The path to the machine file is incorrect: %s \" " % mach_info["machinefile"],
                           "exit 1",
                           "fi"
                           ]   
    
    return "\n".join(header) + "\n"
    
    
    
def get_mpi_call_suffix(mach_info, remote_output_dir):
    
    suffix = []
    
    if "mach_name" in mach_info:
        name = mach_info["mach_name"]
        if name == "vsc3":
            input_dir = os.path.join(remote_output_dir, "mpicfg")
            machinefile = "nodesfile" 
            suffix.append("-machinefile %s" %(os.path.join(input_dir, machinefile)) )       
                
    return " ".join(suffix)
    
    
    
    
    
    


