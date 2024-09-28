import numpy as np
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def k_factors(table_directory, input_sm_csv, input_smeft_csv):
    sm = pd.read_csv(input_sm_csv)
    smeft = pd.read_csv(input_smeft_csv)
    
    # Assuming 'Cross Section' is the column name in both CSVs
    k_factors_df = (sm['Cross Section'] + smeft['Cross Section']) / sm['Cross Section']
    
    # Create a DataFrame from the calculated values
    k_factors_df = pd.DataFrame(k_factors_df)
    
    # Write the calculated means to a new CSV file
    k_factors_df.to_csv(os.path.join(table_directory, 'k_factors.csv'), index=False)
    return k_factors_df

    print(table_directory)
    print(k_factors_df)

def main():
    tables=[1,2,3,4,5,6]
    
    # Initialize an empty DataFrame to store all K-factors
    all_k_factors_df = pd.DataFrame()
    
    for table in tables:
        df_sm = f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_0_NP_eq_0/Table{table}/cross_section_output.csv"
        df_smeft =f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_1_NP_2_eq_2/Table{table}/cross_section_output.csv"
        
        # Define the header information
        header_info = """
 *******************************************************************************************
SetName: CMS_2JET_8TEV_R06
Author: FL
Date: 2024
CodesUsed: madgraph
SMEFTmodel: gluon_dim8_UFO-massless
process: p p > j j NP^2==2
Operator: Og
Coefficient Cg: 1
Lambda: 1000 Gev
PDFset: NNPDF40_nnlo_as_0118
********************************************************************************************
"""
        
        # Calculate K-factors for the current table
        k_factors_df = k_factors( f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_1_NP_2_eq_2/Table{table}/", df_sm, df_smeft)
        
        # Remove the header from the K-factors CSV
        #clean_k_factors_df = remove_header_from_csv(k_factors_df, f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_8TEV_SCRIPTS_CG_1_NP_2_eq_2/Table{table}/clean_k_factors.csv")
        
        # Append the calculated K-factors to the all_k_factors_df DataFrame
        all_k_factors_df = pd.concat([all_k_factors_df, k_factors_df], ignore_index=True)
    
    # Prepend the header information to the DataFrame
    header_rows_df = pd.DataFrame([header_info.split('\n')], columns=['Header'])
    all_k_factors_df = pd.concat([header_rows_df, all_k_factors_df], ignore_index=True)
    
    # Save the concatenated DataFrame to a CSV file
    all_k_factors_df.to_csv(os.path.join("/home/turing/MG5_aMC_v3_4_2/K_FACTORS_CMS_DIJET_8TEV_NP_EQ_0_NP_2_EQ_2/", 'all_k_factors.csv'), index=False)
    
if __name__ == "__main__":
    main()

# Assuming the k_factors function and remove_header_from_csv function are defined elsewhere in your script
