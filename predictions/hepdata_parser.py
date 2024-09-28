import yaml
from misc_utils import str_to_num, from_TeV_to_GeV


#== Note that this dictionary strongly depends on the experiment
#  and should be thus modified accordingly

HEP_to_mg5 = {"ABS(YRAP(JET1))": "etaj", "ABS(YRAP(JET2))": "etaj", 
                "PT(JET1)": "ptj1min", "PT(JET2)": "ptj2min", "R":"drjj",
                "YRAP*": "rapstar", "M(2JET)": "Mdijet"}

def read_exp_cuts(hep_table):
    """
    Note: this function is meant to read tables from 
    the experiment 1312.3524 (see arXiv)

    Given a HEPData yaml table, get the relevant cuts
    
    Parameters
    ----------

    hep_table : str
            path to HEPData yaml runcard

    Returns
    -------

    fixed_cuts : dict
                dictionary containing basic cuts from the experimet
    """

    with open(hep_table,'r') as f:
        card = yaml.load(f, Loader=yaml.FullLoader)
    
    fixed_cuts = {}
    # write cuts of the experiment into dictionary
    # HEP names are changed to mg5 names using HEP_to_mg5 dict
    for item in card['dependent_variables'][0]['qualifiers']:
        if item["name"] in HEP_to_mg5:
            fixed_cuts[HEP_to_mg5[item["name"]]] = str_to_num(item["value"])
    
    return fixed_cuts
    

def read_HEP_data_to_mg5(hep_table):
    """
    Note: this function is meant to read tables from 
    the experiment 1312.3524 (see arXiv)

    Given a HEPData yaml table, get the relevant cuts
    in order to compute smeft cfactor

    Parameters
    ----------

    hep_table : str
            path to HEPData yaml runcard

    Returns
    -------

    fixed_cuts : dict
                dictionary containing basic cuts from the experimet
    
    mjj_bins : list
            list whose elements are dictionaries with keys
            'low' and 'high' for the dijet mass bins
    """
    
    with open(hep_table,'r') as f:
        card = yaml.load(f, Loader=yaml.FullLoader)
    
    fixed_cuts = {}
    # write cuts of the experiment into dictionary
    # HEP names are changed to mg5 names using HEP_to_mg5 dict
    for item in card['dependent_variables'][0]['qualifiers']:
        if item["name"] in HEP_to_mg5:
            fixed_cuts[HEP_to_mg5[item["name"]]] = str_to_num(item["value"])
    
    # get bins of dijet mass (for fixed y* range)
    # convert in GeV if needed
    mjj_bins = card['independent_variables'][0]['values']
    if (card['independent_variables'][0]['header']['units'] == 'TEV'):
        for bin in mjj_bins:
            bin['high'] = from_TeV_to_GeV(bin['high'])
            bin['low'] = from_TeV_to_GeV(bin['low'])
    
    return fixed_cuts, mjj_bins
