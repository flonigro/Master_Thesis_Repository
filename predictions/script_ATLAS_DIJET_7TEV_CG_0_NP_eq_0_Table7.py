import subprocess
import os
import sys
import glob
import logging
import yaml

sys.path.insert(0, "/home/turing/MG5_aMC_v3_4_2/dijet/dev")
from misc_utils_7TEV_ATLAS_DIJET_CG_0_NP_eq_0 import (modify_value_in_file, print_to_file)
import logging

log = logging.getLogger(__name__)

# Assuming read_HEP_data_to_mg5 is imported or defined somewhere above
from hepdata_parser_7TEV_ATLAS_DIJET_CG_0_NP_eq_0 import read_HEP_data_to_mg5

import yaml

def get_launch_card(mjj, ystarmax, ystarmin, fixed_cuts, nevents=10000, lhaid=331100, pdlabel="lhapdf", dynamical_scale_choice=4, ebeam1=3500, ebeam2=3500, output_name=None):
    launch = (
    "set automatic_html_opening False\n" + \
    "launch\n" + \
    f"set run_tag ystar_{ystarmin}"+f"_{ystarmax}"+f"_mjj_{mjj['low']}"+f"_{mjj['high']}"\
                +f"_R_{fixed_cuts['drjj']}\n" + \
    f"set nevents {nevents}\n" + \
    f"set ebeam1 {ebeam1}\n" + \
    f"set ebeam2 {ebeam2}\n" + \
    f"set pdlabel {pdlabel}\n" + \
    f"set lhaid {lhaid}\n" + \
    f"set dynamical_scale_choice {dynamical_scale_choice}\n" + \
    f"set ptj1min {fixed_cuts['ptj1min']}\n" + \
    f"set ptj2min {fixed_cuts['ptj2min']}\n" + \
    f"set mmjj {mjj['low']}\n" + \
    f"set mmjjmax {mjj['high']}\n" + \
    f"set drjj {fixed_cuts['drjj']}\n" + \
    f"set etaj {fixed_cuts['etaj']}\n" + \
    "set use_syst False"
    )
    return launch

def run_mg5(fixed_cuts, mjj_bins, path_to_mg5_folder, ystarmax, ystarmin, nevents=10000, lhaid=331100, pdlabel="lhapdf", dynamical_scale_choice=4, ebeam1=3500, ebeam2=3500):
    ystarmin = fixed_cuts['rapstar'][0]
    ystarmax = fixed_cuts['rapstar'][1]
    output_dir = os.path.join(path_to_mg5_folder, "Output")
    os.makedirs(output_dir, exist_ok=True)
    
    for i, mjj in enumerate(mjj_bins):
        output_name = f"ATLAS_DIJET_7TEV_CG_0__Y*{ystarmin}_{ystarmax}_mjj_{mjj['low']}_{mjj['high']}_seq{i}"
        launch_card = get_launch_card(mjj, ystarmax, ystarmin, fixed_cuts, nevents, lhaid, pdlabel, dynamical_scale_choice, ebeam1, ebeam2, output_name=output_name)
        
        filename = os.path.join(output_dir, "SubProcesses/cuts.f")
        modify_value_in_file(filename, 'rapstarmin', ystarmin)
        modify_value_in_file(filename, 'rapstarmax', ystarmax)

        command = f"{os.path.join(path_to_mg5_folder, 'bin/madevent')} launch"
        subprocess.run(command, check=True, shell=True, cwd=os.path.join(path_to_mg5_folder, "SubProcesses"))
        log.info(f"MG5 simulation for mjj range {mjj['low']} - {mjj['high']} launched successfully.")

def generate_mjj_launch_cards(mjj_bins, base_path, ystarmin, ystarmax):
    output_dir = os.path.join(base_path)
    os.makedirs(output_dir, exist_ok=True)

    for mjj_bin in mjj_bins:
        script_filename = os.path.join(output_dir, f"script_{mjj_bin['low']}_{mjj_bin['high']}.txt")
        with open(script_filename, 'w') as script_file:
            launch_card = (
        "import model gluon_dim8_UFO-massless\n"
        "generate p p > j j NP=0 QCD==2\n"
        f"output ATLAS_DIJET_7TEV_CG_0_NP_eq_0_Y_{ystarmin}_{ystarmax}_mjj_{mjj_bin['low']}_{mjj_bin['high']}\n"
        "launch\n"
        f"set run_tag ATLAS_DIJET_7TEV_cG_0_NP_eq_0_Y_{ystarmin}_{ystarmax}_mjj_{mjj_bin['low']}_{mjj_bin['high']}\n"
        "set nevents 10000\n"
        "set cG 0.0\n"
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
        "set etaj 3\n"
        "set use_syst False\n"
            )
            script_file.write(launch_card)
            script_file.write("\n")

def create_shell_script(base_path):
    scripts_base_path = os.path.join(base_path, "scripts")
    os.makedirs(scripts_base_path, exist_ok=True)
    
    table_dir = os.path.join("/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0", "Table8")
    script_subdir = os.path.join(table_dir)
    os.makedirs(script_subdir, exist_ok=True)
        
    script_name = f"table8_script.sh"
    script_path = os.path.join(script_subdir, script_name)
        
    with open(script_path, 'w') as script_file:
        script_file.write("#!/bin/bash\n")
        script_file.write(f"for script_file in $(ls *.txt); do\n")
        script_file.write("    script_name=$(basename $script_file)\n")
        script_file.write("    echo \"Running MG5 simulation for $script_name...\"\n")
        script_file.write("../../../MG5_aMC_v3_4_2/bin/mg5_aMC $script_name\n")
        script_file.write("done\n")
        
    os.chmod(script_path, 0o755)

def run_all_sh_scripts(base_path):
    sh_files = glob.glob(os.path.join(base_path, '*.sh'))
    
    for sh_file in sh_files:
        abs_sh_path = os.path.abspath(sh_file)
        print(f"Executing script: {abs_sh_path}")
        try:
            os.chdir(os.path.dirname(abs_sh_path))
            subprocess.run([abs_sh_path], check=True)
            print(f"Script {abs_sh_path} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute script {abs_sh_path}: {e}")
        finally:
            os.chdir(os.getcwd())

def main():
    yaml_files_directory = "/home/turing/MG5_aMC_v3_4_2/dijet/data/rawdata/ATLAS_2JET_7TEV_R06_rawdata/"
    yaml_files = glob.glob(os.path.join(yaml_files_directory, "*.yaml"))

    table_values = {
        8: (0.5, 1.0)
    }

    tables = [8]

    for yaml_file in yaml_files:
        base_filename = os.path.basename(yaml_file).strip()
        table_number = int(base_filename.split('_')[-1].split('.')[0])
        if table_number in tables:
            fixed_cuts, mjj_bins = read_HEP_data_to_mg5(yaml_file)
            ystarmin = fixed_cuts['rapstar'][0]
            ystarmax = fixed_cuts['rapstar'][1]
            path_to_script = os.path.join('/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0', f'Table{table_number}')
            os.makedirs(path_to_script, exist_ok=True)
            generate_mjj_launch_cards(mjj_bins, path_to_script, ystarmin, ystarmax)
            create_shell_script(path_to_script)
        else:
            logging.error(f"Unsupported YAML file: {yaml_file}, skipping.")

    script_dirs = ['/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/Table8/']
    run_all_sh_scripts(script_dirs[0])  # Execute shell scripts for Table8 only

if __name__ == "__main__":
    main()
