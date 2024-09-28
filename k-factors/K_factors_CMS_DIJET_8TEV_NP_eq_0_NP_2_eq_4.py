import pandas as pd
import numpy as np
import csv
import os
def k_factors(table_directory, input_sm_csv, input_smeft_csv):
    sm = pd.read_csv(input_sm_csv)
    smeft = pd.read_csv(input_smeft_csv)
    
    # Calculate the k-factors
    k_factors_df = (sm['Values'] + smeft['Values']) / sm['Values']
    
    # Initialize the values array with zeros, matching the length of k_factors_df
    values = np.zeros(len(k_factors_df))
    
    # Insert the values array as a new column in the DataFrame
    # Ensure the DataFrame has enough columns to insert the new column at position 2
    k_factors_df = pd.concat([k_factors_df, pd.DataFrame(values, columns=['NewColumn'])], axis=1)
    
    # Write the calculated means to a new CSV file
    k_factors_df.to_csv(os.path.join(table_directory, 'k_factors.csv'), index=False)
    print(k_factors_df)
    return k_factors_df

import pandas as pd

def remove_header_from_csv(file_path, output_file_path):
    '''
    with open(file_path, "r") as infile, open(output_file_path, "w", newline='') as outfile:
        reader = csv.reader(infile)
        next(reader) 
        writer = csv.writer(outfile)
        for row in reader:
            # process each row
            writer.writerow(row)
            print(row)
    '''
    """
    Read a CSV file into a DataFrame, remove the header, round numbers to the 5th decimal place,
    and save the result to another file.
    """
    # Read the CSV file into a DataFrame, keeping the header
    df = pd.read_csv(file_path)
    df = pd.read_csv(file_path, skiprows=1)
    # Remove the header row from the DataFrame
    
    # Round all numeric values to the 5th decimal place
    df = df.round(5)
    
    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file_path, index=False)
    return df
    # Print the first few rows of the modified DataFrame
    print(df)
    
    #return df

def main():
    tables = [1, 2, 3, 4, 5, 6]
    
    all_k_factors_df = pd.DataFrame()
    
    for table in tables:
        df_sm = f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_0_NP_eq_0/Table{table}/cross_section_output_sorted_rel.csv"
        df_smeft = f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/cross_section_output_sorted_rel.csv"
        
        k_factors_df = k_factors( f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/", df_sm, df_smeft)
        clean_k_factors_df = remove_header_from_csv(f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/k_factors.csv", f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/clean_k_factors.csv")
        all_k_factors_df = pd.concat([all_k_factors_df, clean_k_factors_df])
        #all_k_factors_df = pd.concat([all_k_factors_df, clean_k_factors_df])
    
    # Prepend the header information to the final output file
    header_info = """*******************************************************************************************
Set Name: CMS_2JET_8TEV_R07
Author: FL
Date: 2024
Codes Used: madgraph
SMEFT Model: gluon_dim8_UFO-massless
Process: p p > j j NP^2==2
Operator: Og
Coefficient Cg: 1
Lambda: 1000 GeV
PDF Set: NNPDF40_nnlo_as_0118
*******************************************************************************************"""

    with open("/home/turing/MG5_aMC_v3_4_2/K_FACTORS_CMS_DIJET_8TEV_NP_EQ_0_NP_2_EQ_4/all_k_factors.csv", "w") as outfile:
        outfile.write(header_info)
        outfile.write("\n")
        all_k_factors_df.to_csv(outfile, index=False)

if __name__ == "__main__":
    main()

