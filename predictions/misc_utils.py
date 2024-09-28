import numpy as np
import fileinput
import re

def bin_middle(bin_edges):
    """
    given binedges return bin middle

    Returns
    -------
    np.array
    """
    bin_mid = [0.5 * (bin_edges[i] + bin_edges[i+1]) 
                for i in range(len(bin_edges)-1)]
    return np.array(bin_mid)


def range_str_to_floats(str_range):
    """
    converts a string range to a list,
    e.g. "0.5 - 1.0" --> [0.5,1.0]
    """
    # Split the range string into two parts
    str_nums = str_range.split('-')
    # Convert the parts to floats
    num1 = float(str_nums[0])
    num2 = float(str_nums[1])
    # Return a list of the floats
    return [num1, num2]


def str_to_num(str_num):
    """
    if input string of type '< num'
    return num, where num is any float

    else if string range convert to list
    """

    # Remove any whitespace from the input string
    str_num = str_num.strip()
    # Check if the string is a range string (e.g. '0.5-1.0')
    if '-' in str_num:
        # If so, call the range string function and return the result
        return range_str_to_floats(str_num)
    # Check if the string starts with a comparison operator
    elif str_num.startswith(('>', '<', '>=', '<=')):
        # If so, remove the operator and any whitespace that follows
        str_num = str_num[1:].lstrip()
    # Convert the remaining string to a number (int or float)
    num = float(str_num)
    if num.is_integer():
        num = int(num)
    # Return the number
    return num


from_TeV_to_GeV = lambda x: 1e3 * x




def modify_value_in_file(filename, varname, newvalue):
    """
    Given a file in which some variables are declared
    as `var = ...` search for places in which a specific
    variable (varname) has been assigned to a value
    and change the old value to newvalue.
    The input file is rewritten with updated variable value

    Parameters
    ----------

    filename : str
            path to file, e.g. path to SubProcesses/cuts.f
    
    varname : str
            name of the variable to search
    
    newvalue : str, int, float, list...
            new value to be assigned to the variable

    """
    # Compile a regular expression pattern to match the variable declaration
    pattern = re.compile(r"\b{} = \S+".format(varname))

    # Loop over the lines in the file and replace the variable value if found
    for line in fileinput.input(filename, inplace=True):
        if pattern.search(line):
            # Replace the old value with the new value
            line = re.sub(r"\b\S+$", str(newvalue), line)
        # Write the modified line to the file
        print(line, end="")

def print_to_file(string,namefile):
    """
    given a string, print it to a file.
    Note file gets overwritten
    
    Parameters
    ----------

    string : str
            string to be appended to file

    namefile : str
            path to file
        
    """
    with open(namefile,"w") as file:
        file.write(string)


if __name__ == "__main__":
    filename = "/Users/markcostantini/codes/MG5_aMC_v2_8_2/gghg_Born/SubProcesses/cuts.f"
    varname = "pappapero"
    newvalue = 200
    modify_value_in_file(filename, varname, newvalue)



