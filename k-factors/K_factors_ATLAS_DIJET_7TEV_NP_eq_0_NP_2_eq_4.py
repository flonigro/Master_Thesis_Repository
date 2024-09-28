import os
import pandas as pd
import os
import numpy as np
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cross_sections_vs_mjj_with_global_uncertainties(csv_file_path_real, csv_file_path_extracted, csv_file_path_extracted_lin, csv_file_path_diff,label):
    dir_name = os.path.dirname(csv_file_path_extracted)
    label_dir = os.path.join(dir_name, label)
    os.makedirs(label_dir, exist_ok=True)
    
    plot_filename = os.path.basename(csv_file_path_extracted).replace('.csv', '.png')
    plot_filepath = os.path.join(label_dir, plot_filename)
    df_extracted = pd.read_csv(csv_file_path_extracted)
    df_extracted_lin = pd.read_csv(csv_file_path_extracted_lin)
    df_real = pd.read_csv(csv_file_path_real)
    df_range = pd.read_csv(csv_file_path_diff)
    
    fig, axs = plt.subplots(2, figsize=(10, 12), gridspec_kw = {'wspace':0, 'hspace':0, 'height_ratios':[3,1]}, sharex=True)
    #gs = gridspec.GridSpec(1, 2, height_ratios=[5,2])
    #plt.subplots_adjust(wspace=0, hspace=0)
    
    axs[0].set_xscale("linear")  # Set x-scale to linear
    axs[0].set_yscale("log")
    axs[0].errorbar(df_real['Mean'], df_real['Cross Section'], xerr=(df_range['Diff']), linestyle='None', marker='^', capsize=3, label=f'{label} Data with Global Uncertainties')
    axs[0].scatter(df_real['Mean'], (df_extracted['Values']), c='red', alpha=0.6, label='Theoretical Quadratic Predictions')
    axs[0].scatter(df_real['Mean'], df_extracted_lin['Cross Section'], c='green', alpha=0.6, label ='Theoretical Linear Predictions')
    
    #axs[0].set_ylim(-0.1, 0.1)
    axs[0].set_ylabel('Cross Section [pb/GeV]')
    axs[0].set_title(f'Cross Sections vs MJJMax with Global Uncertainties ({label})')
    axs[0].legend(loc='upper right')
    axs[0].grid(True)

    # Second subplot: Ratio of Cross Sections vs MJJMax
    axs[1].set_xscale
    axs[1].set_yscale
    axs[1].errorbar(df_real['Mean'], ((df_extracted['Values']+df_real['Cross Section'])/df_real['Cross Section']),linestyle='None', marker='^', capsize=3, label="Ratio")
    axs[1].set_xlabel('MJJ [GeV]')
    axs[1].set_ylabel('Ratio SMEFT over SM')
    #axs[1].set_xlim(0, 4
    #axs[1].set_ylim(0.8,1.2)
    #axs[1].set_title(f'Ratio: data/theory ({label})')
    axs[1].legend(loc='upper right')
    axs[1].grid(True)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  
    plt.savefig(plot_filepath, dpi=300, bbox_inches='tight')
    plt.show()  


def plot_correlation(csv_file_path_real,csv_file_path_extracted, label):
    
    df_extracted = pd.read_csv(csv_file_path_extracted)
    df_real = pd.read_csv(csv_file_path_real)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap((df_extracted['Values'], df_real['Cross Section']), annot=False, cmap='coolwarm', cbar_kws={'label': 'Correlation'})
    plt.title(f'Correlation between Cross Section and MJJ ({label})')
    plt.xlabel(df_extracted['Values'])
    plt.ylabel(df_real['Cross Section'])
    plt.show()
    
def k_factors(table_directory, input_sm_csv, input_smeft_csv):
    sm = pd.read_csv(input_sm_csv)
    smeft = pd.read_csv(input_smeft_csv)
    
    # Calculate the k-factors
    k_factors_df = (sm['Values'] + smeft['Values']).round(5)
    
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
        df_sm = f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/Table{table}/cross_section_output_sorted_rel.csv"
        df_merged_sm  = f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/Table{table}/merged_output_sorted_NEW.csv"
        df_smeft =f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/cross_section_output_sorted_rel.csv"
        df_smeft_lin =f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_2/Table{table}/cross_section_output_sorted.csv" 
        label = None
        if table == 7:
            label = "0.0_y__0.5"
        elif table == 8:
            label = "0.5_y__1.0"
        elif table == 9:
            label = "1.0_y__1.5"
        elif table == 10:
            label = "1.5_y__2.0"
        elif table == 11:
            label = "2.0_y__2.5"
        elif table == 12:
            label = "2.5_y__3.0"
        df_diff = f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/Table{table}/MJJDiff_NEW_NEW_NEW{label}.csv"
        
        header_info = """*******************************************************************************************
SetName: ATLAS_2JET_7TEV_R06
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
        
        k_factors_df = k_factors( f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/", df_sm, df_smeft)
        clean_k_factors_df = remove_header_from_csv(f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/k_factors.csv", f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_4/Table{table}/clean_k_factors.csv")
        all_k_factors_df = pd.concat([all_k_factors_df, clean_k_factors_df])
        
        plot_cross_sections_vs_mjj_with_global_uncertainties(df_merged_sm, df_smeft, df_smeft_lin, df_diff,label)
        plot_correlation(df_merged_sm, df_smeft, label)
        
    with open(os.path.join(f"/home/turing/MG5_aMC_v3_4_2/K_FACTORS_ATLAS_DIJET_7TEV_NP_EQ_0_NP_2_EQ_4/all_sum.csv"), "w") as outfile:
        outfile.write(header_info)
        outfile.write("\n")  
        all_k_factors_df.to_csv(outfile, index=False)

if __name__ == "__main__":
    main()
