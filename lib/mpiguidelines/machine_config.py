
import os
import sys

    
def get_mpi_call(nodes, nnp, mach_info):
    call = ""

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

        call = "%s/mpirun -np %d -ppn %s %s -machinefile %s" \
            % ( mach_info["mpi_path"], np, nnp, pin_option, mach_info["machinefile"])

    elif mach_info["mpiimpl"] == "mpich":       # MVAPICH calls to mpirun
        np = nodes * nnp
        
        # remove pinning option if not required
        pin_option = "-bind-to rr"
        if mach_info["pinning"] == "nopin":
            pin_option = ""

        call = "%s/mpirun -np %d -ppn %s %s -machinefile %s" \
            % ( mach_info["mpi_path"], np, nnp, pin_option, mach_info["machinefile"])

    return call

