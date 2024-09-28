import subprocess
import os
import sys
import glob
import logging
import yaml
#from collections import defaultdict  
sys.path.insert(0, "/home/turing/MG5_aMC_v3_4_2/dijet/dev")
from misc_utils_7TEV_ATLAS_DIJET_CG_0_NP_eq_0 import (modify_value_in_file, print_to_file)
import logging

log = logging.getLogger(__name__)

# Assuming read_HEP_data_to_mg5 is imported or defined somewhere above
from hepdata_parser_7TEV_ATLAS_DIJET_CG_0_NP_eq_0 import read_HEP_data_to_mg5

import yaml
import os
import subprocess
import logging as log

def generate_mjj_launch_cards(mjj_bins, base_path, ystarmin, ystarmax):
    output_dir = os.path.join(base_path)
    os.makedirs(output_dir, exist_ok=True)

    for mjj_bin in mjj_bins:
        script_filename = os.path.join(output_dir, f"script_{mjj_bin['low']}_{mjj_bin['high']}.txt")
        with open(script_filename, 'w') as script_file:
            launch_card = (
        "import model gluon_dim8_UFO-massless\n"
        "generate p p > j j NP^2==4\n"
        f"output ATLAS_DIJET_7TEV_R06_Y_{ystarmin}_{ystarmax}_mjj_{mjj_bin['low']}_{mjj_bin['high']}\n"
        "launch\n"
        f"set run_tag ATLAS_DIJET_7TEV_R06_Y_{ystarmin}_{ystarmax}_mjj_{mjj_bin['low']}_{mjj_bin['high']}\n"
        "set nevents 10000\n"
        "set cG 1.0\n"
        "set cG1 0.0\n"
        "set cG2 0.0\n"
        "set cG3 0.0\n"
        "set cG4 0.0\n"
        "set cG5 0.0\n"
        "set cG6 0.0\n"
        "set cG7 0.0\n"
        "set cG8 0.0\n"
        "set cG9 0.0\n"
        f"set ebeam1 3500.0\n"
        f"set ebeam2 3500.0\n"
        "set pdlabel lhapdf\n"
        "set lhaid 331100\n"
        "set dynamical_scale_choice 4\n"
        "set ptj1min 100.0\n"
        "set ptj2min 50.0\n"
        f"set mmjj {mjj_bin['low']}\n"
        f"set mmjjmax {mjj_bin['high']}\n"
        "set drjj 0.6\n"
        f"set etaj 3.0\n"
        f"set etajmin {ystarmin}\n"
        "set use_syst False\n"
            )
            script_file.write(launch_card)
            script_file.write("\n")

def create_shell_script(base_path):
    # Define the base path where the scripts will be stored
    scripts_base_path = os.path.join(base_path, "scripts")
    os.makedirs(scripts_base_path, exist_ok=True)  # Ensure the directory exists
    
    # Directly specify the target directory for each script based on the table number
    for table_number in range(7, 13):  # Loop from 7 to 12 for Table7 to Table12
        table_dir = os.path.join("/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_4", f"Table{table_number}")
        script_subdir = os.path.join(table_dir)  # Adjusted to match the expected structure
        os.makedirs(script_subdir, exist_ok=True)  # Create a subdirectory for the script
        
        script_name = f"table{table_number}_script.sh"
        script_path = os.path.join(script_subdir, script_name)
        
        # Open the script file in write mode
        with open(script_path, 'w') as script_file:
            script_file.write("#!/bin/bash\n")
            script_file.write(f"for script_file in $(ls *.txt); do\n")  # Adjusted to correctly locate scripts.txt files
            
            
            # Write the rest of the script content
            script_file.write("    script_name=$(basename $script_file)\n")
            script_file.write("    echo \"Running MG5 simulation for $script_name...\"\n")
            script_file.write("../../../MG5_aMC_v3_4_2/bin/mg5_aMC $script_name\n")
            script_file.write("done\n")
        
        # Change the permissions of the script file to make it executable
        os.chmod(script_path, 0o755)
import os
import glob
import subprocess
import logging

def run_all_sh_scripts(fixed_cuts, base_path, ystarmax, ystarmin):
    sh_files = glob.glob(os.path.join(base_path, '*.sh'))
    ystarmin = fixed_cuts['rapstar'][0]
    ystarmax = fixed_cuts['rapstar'][1]
    
   
    # Path to the cuts.f file within the SubProcesses directory
    path_to_cuts = ("/home/turing/MG5_aMC_v3_4_2/Template/LO/SubProcesses/cuts.f")
    #path_to_launch = ("/home/turing/MG5_aMC_v3_4_2/Template/LO/launch")
    
    # Modify the cuts.f file before running the script
    modify_value_in_file(filename=path_to_cuts, varname='rapstarmax', newvalue=ystarmax)
    modify_value_in_file(filename=path_to_cuts, varname='rapstarmin', newvalue=ystarmin)
    print("rapstarmin", ystarmin)
    print("rapstarmax", ystarmax)
    for sh_file in sh_files:
        abs_sh_path = os.path.abspath(sh_file)
        log.info(f"Executing script: {abs_sh_path}")
        try:
            os.chdir(os.path.dirname(abs_sh_path))
            subprocess.run([abs_sh_path], check=True)
            log.info(f"Script {abs_sh_path} executed successfully.")
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to execute script {abs_sh_path}: {e}")
        finally:
            os.chdir(os.getcwd())
     

import os
import glob
import logging


def main():
    yaml_files_directory = "/home/turing/MG5_aMC_v3_4_2/dijet/data/rawdata/ATLAS_2JET_7TEV_R06_rawdata/"
    yaml_files = glob.glob(os.path.join(yaml_files_directory, "*.yaml"))

    table_values = {
        7: (0.0, 0.5),
        8: (0.5, 1.0),
        9: (1.0, 1.5),
        10: (1.5, 2.0),
        11: (2.0, 2.5),
        12: (2.5, 3.0),
    }

    tables = [7, 8, 9, 10, 11, 12]

    for yaml_file in yaml_files:
        base_filename = os.path.basename(yaml_file).strip()
        table_number = int(base_filename.split('_')[-1].split('.')[0])
        if table_number in tables:
            ystarmin, ystarmax = table_values[table_number]
            fixed_cuts, mjj_bins = read_HEP_data_to_mg5(yaml_file)
            path_to_script = os.path.join('/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_4', f'Table{table_number}')
            os.makedirs(path_to_script, exist_ok=True)
            generate_mjj_launch_cards(mjj_bins, path_to_script, ystarmin, ystarmax)
            create_shell_script(path_to_script)  # Create shell scripts for each table
            run_all_sh_scripts(fixed_cuts, path_to_script, ystarmax=ystarmax, ystarmin=ystarmin)
        else:
            logging.error(f"Unsupported YAML file: {yaml_file}, skipping.")

  
if __name__ == "__main__":
    main()
