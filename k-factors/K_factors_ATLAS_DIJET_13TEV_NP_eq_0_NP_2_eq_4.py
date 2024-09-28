import os
import pandas as pd
import os
import numpy as np
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def k_factors(table_directory, input_sm_csv, input_smeft_csv):
    sm = pd.read_csv(input_sm_csv)
    smeft = pd.read_csv(input_smeft_csv)
    
    # Calculate the k-factors
    k_factors_df = ((sm['Values'] + smeft['Values']) / sm['Values']).round(5)
    
    # Initialize the values array with zeros, matching the length of k_factors_df
    values = (np.zeros(len(k_factors_df))).round(5)
    
    # Insert the values array as a new column in the DataFrame
    # Ensure the DataFrame has enough columns to insert the new column at position 2
    k_factors_df = pd.concat([k_factors_df, pd.DataFrame(values, columns=['NewColumn'])], axis=1)
    
    # Write the calculated means to a new CSV file
    k_factors_df.to_csv(os.path.join(table_directory, 'k_factors.csv'), index=False)
    print(k_factors_df)
    return k_factors_df

def remove_header_from_csv(file_path, output_file_path):
    """
    Remove the header from a CSV file and save the result to another file.
    
    Parameters:
    - file_path (str): Path to the input CSV file.
    - output_file_path (str): Path to the output CSV file without the header.
    """
    # Read the CSV file into a DataFrame
    #k_factors_df = pd.read_csv(file_path)
    clean_k_factors_df = pd.read_csv(file_path, skiprows=1)
    
    # Save the modified DataFrame to a new CSV file
    clean_k_factors_df.to_csv(output_file_path, index=False)
    print(clean_k_factors_df)
    return clean_k_factors_df

def main():
    tables=[7,8,9,10,11,12]
    
    all_k_factors_df = pd.DataFrame()
    
    for table in tables:
        df_sm = f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_13TEV_SCRIPTS_CG_0_NP_eq_0/Table{table}/cross_section_output_sorted_rel.csv"
        df_smeft =f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_13TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/cross_section_output_sorted_rel.csv"
        
        header_info = """*******************************************************************************************
SetName: ATLAS_2JET_13TEV_R06
Author: FL
Date: 2024
CodesUsed: madgraph
SMEFTmodel: gluon_dim8_UFO-massless
process: p p > j j NP^2==4
Operator: Og
Coefficient Cg: 1
Lambda: 1000 Gev
PDFset: NNPDF40_nnlo_as_0118
********************************************************************************************"""
        
        k_factors_df = k_factors( f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_13TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/", df_sm, df_smeft)
        clean_k_factors_df = remove_header_from_csv(f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_13TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/k_factors.csv", f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_13TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/clean_k_factors.csv")
        all_k_factors_df = pd.concat([all_k_factors_df, clean_k_factors_df])
    
    # Prepend the header information to the final output file
    with open(os.path.join(f"/home/turing/MG5_aMC_v3_4_2/K_FACTORS_ATLAS_DIJET_13TEV_NP_EQ_0_NP_2_EQ_4/all_k_factors.csv"), "w") as outfile:
        outfile.write(header_info)
        outfile.write("\n")  # Add one newline to separate the header from the data
        all_k_factors_df.to_csv(outfile, index=False)

if __name__ == "__main__":
    main()
