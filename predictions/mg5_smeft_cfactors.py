"""
Given a HEPData file in yaml format, 
run Madgraph to compute a Smeft c-factor
with the same kinematics.
"""

import subprocess
import yaml
from misc_utils import (modify_value_in_file, print_to_file)
import logging

log = logging.getLogger(__name__)


def get_launch_card(
            mjj,ystarmax,ystarmin,fixed_cuts,
            nevents = 1000, lhaid = 331700,
            pdlabel="lhapdf",
            dynamical_scale_choice = 3,
            ebeam1= 3500, ebeam2 = 3500
            ):
    """
    get launch card to be passed to mg5 binary



    Parameters
    ----------

    mjj : dict
        dictionary containing one dijet mass bin.
        Key 'low' for lower bin
        Key 'high' for upper bin
    
    ystarmax : float
    
    ystarmin : float
    
    fixed_cuts : dict
            dictionary containing the basic experimental cuts

    nevents : int, default =  1000
            number of MC events for one bin for mg5 integration 
    
    lhaid : int, default = 331700
            lhaid, default corresponds to NNPDF40_nlo_as_01180

    dynamical_scale_choice : int, default = 3 --> subm of transverse mass / 2
                dynamical scale choice in madgraph.
                See SubProcesses/setscales.f for more details


    Returns
    -------
    str, launch card with correct formatting

    """

    launch = \
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

    return launch


def run_mg5(
            fixed_cuts,mjj_bins,path_to_mg5_folder, 
            nevents = 1000, lhaid = 331700,
            pdlabel="lhapdf",
            dynamical_scale_choice = 3,
            ebeam1= 3500, ebeam2 = 3500
            ):
    """


    Parameters
    ----------

    path_to_mg5_folder :

    fixed_cuts :
    
    mjj_bins :
    
    nevents :
    
    lhaid :
    
    dynamical_scale_choice :


    """
    
    # change rapstarmin and rapstarmax in SubProcesses/cuts.f
    #  in order to run within the correct y* bin
    ystarmin = fixed_cuts['rapstar'][0]
    ystarmax = fixed_cuts['rapstar'][1]
    path_to_cuts = path_to_mg5_folder + "/SubProcesses/cuts.f"
    modify_value_in_file(filename=path_to_cuts, varname='rapstarmin', newvalue=ystarmin)
    modify_value_in_file(filename=path_to_cuts, varname='rapstarmax', newvalue=ystarmax)

    for mjj in mjj_bins:

        launch = get_launch_card(
            mjj,ystarmax,ystarmin,fixed_cuts,
            nevents, lhaid,
            pdlabel
            dynamical_scale_choice,
            ebeam1, ebeam2
            )

        # overwrite launch card with updated launch card
        print_to_file(launch,path_to_mg5_folder+"/launch")

        # run mg5 with launch card and wait until Event generation is done
        log.info(f"Running Process with y* = [{ystarmin,ystarmax}] and mjj = [{mjj['low'],mjj['high']}]")
        command = f"{path_to_mg5_folder}/bin/madevent launch"
        proc = subprocess.Popen(command, shell = True)
        proc.wait() 



if __name__ == "__main__":
    from hepdata_parser import read_HEP_data_to_mg5
    hep_table = "/Users/markcostantini/Projects/PhD/smeft_jets/smeftjet_dev/HEPData-ins1268975-v1-Table_8.yaml"
    fixed_cuts, mjj_bins = read_HEP_data_to_mg5(hep_table)

    launch = get_launch_card(
            mjj = {'low':200, 'high':400},ystarmax=0.5,ystarmin = 0.0,
            fixed_cuts = fixed_cuts, nevents = 1000, lhaid = 331700,
            dynamical_scale_choice = 3
            )

    print(launch)
    # run_mg5(fixed_cuts,mjj_bins)

    




# if __name__ == "__main__":
#     cd_file = "/Users/markcostantini/miniconda3/envs/nnpdf-dev/share/NNPDF/data/commondata/DATA_ATLAS_2JET_7TEV_R06.dat"
#     sys_file = "/Users/markcostantini/miniconda3/envs/nnpdf-dev/share/NNPDF/data/commondata/systypes/SYSTYPE_ATLAS_2JET_7TEV_R06_DEFAULT.dat"
#     setname = "ATLAS_2JET_7TEV_R06"
#     run_mg5()

