import os
import numpy as np
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
import csv
import re
#labels = ["0.0<y*<0.5", "0.5<y*<1.0", "1.0<y*<1.5", "1.5<y*<2.0", "2.0<y*<2.5", "2.5<y*<3.0"]

import os
import re
import csv
'''
def extract_cross_sections_and_save_csv(output_dirs, csv_file_path):
    cross_sections = []

    for directory in output_dirs:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith("run_01") and "_banner.txt" in file:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as txt_file:
                        lines = txt_file.readlines()
                        for line in lines:
                            if "Integrated weight (pb)" in line:
                                cross_section_match = re.search(r':\s+(\d+\.\d+e-\d+)', line)
                                if cross_section_match:
                                    # Convert the matched value to float and then to a formatted string
                                    cross_section_value = float(cross_section_match.group(1))
                                    formatted_cross_section = "{:.10f}".format(cross_section_value)  # Adjust the precision as needed
                                    cross_sections.append(formatted_cross_section)

    # Sort the cross-section values in descending order
    cross_sections.sort(reverse=True)

    with open(csv_file_path, mode='w', newline='') as csvfile:
        fieldnames = ['Cross Section']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for cross_section in cross_sections:
            writer.writerow({'Cross Section': cross_section})
'''
def sort_cross_section_csv(csv_file_input, csv_file_output):
    """
    Loads a CSV file into a DataFrame, sorts it by the "Cross Section" column in descending order,
    and saves the sorted DataFrame to a new CSV file named 'cross_section_output_sorted.csv'.
    
    Parameters:
    - directory (str): Directory where the CSV file is located.
    
    Returns:
    None
    """
    #csv_file_path = f"{directory}/cross_section_output.csv"
    df = pd.read_csv(csv_file_input)
    
    # Sort the DataFrame by the "Cross Section" column in descending order
    df_sorted = df.sort_values(by="Cross Section", ascending=False)
    
    # Define the new file path for the sorted CSV
    #sorted_csv_file_path = f"{directory}/cross_section_output_sorted.csv"
    
    # Save the sorted DataFrame to the new CSV file
    df_sorted.to_csv(csv_file_output, index=False)
    print(f"Sorted CSV file has been successfully saved to {csv_file_output}")
    



import csv
'''
import csv
def save_mjj_mean_values(table_directory, label, input_mjj_low_csv, input_mjj_high_csv):
    #table_directory = os.path.join(output_base_dir)
    #if not os.path.exists(table_directory):
    #    os.makedirs(table_directory)
    
    #file_name = f'MJJMean_Real{label}.csv'
    #file_path = table_directory

    mjj_low_df = pd.read_csv(input_mjj_low_csv)
    mjj_high_df = pd.read_csv(input_mjj_high_csv)

    # Ensure both DataFrames have the same structure and columns
    #assert set(mjj_low_df.columns) == set(mjj_high_df.columns), "DataFrames have different columns"

    # Calculate the mean between corresponding rows from both DataFrames
    # Assuming the columns to take the mean of are named 'ColumnToTakeMeanOf'
    # Replace 'ColumnToTakeMeanOf' with the actual column name(s) you want to average
        
    mean_df = (mjj_low_df['MJJMin'] + mjj_high_df['MJJMax'])/2

    mean_df = pd.DataFrame(mean_df, columns=['Mean'])

    # Write the calculated means to a new CSV file
    mean_df.to_csv(table_directory, index=False)

def save_crosssection_deltamjj_deltay_values(output, label, input_cross_sections_csv, input_deltamjj_deltay_csv):
    #table_directory = output
    #if not os.path.exists(table_directory):
     #   os.makedirs(table_directory)
        
    #file_name = f'CrossSections_DeltaMjj_DeltaY_NEW_NEW_NEW{label}.csv'
    file_path = output

    mjj_cross_section_df = pd.read_csv(input_cross_sections_csv)
    mjj_deltamjj_deltay_df = pd.read_csv(input_deltamjj_deltay_csv)

    # Ensure both DataFrames have the same structure and columns
    #assert set(mjj_low_df.columns) == set(mjj_high_df.columns), "DataFrames have different columns"

    # Calculate the mean between corresponding rows from both DataFrames
    # Assuming the columns to take the mean of are named 'ColumnToTakeMeanOf'
    # Replace 'ColumnToTakeMeanOf' with the actual column name(s) you want to average
        
    ratio_df = (mjj_cross_section_df['Cross Section'])/(mjj_deltamjj_deltay_df['Diff'])

    ratio_df = pd.DataFrame(ratio_df, columns=['Cross Section'])

    # Write the calculated means to a new CSV file
    ratio_df.to_csv(file_path, index=False)
    
def merge_csv_files(input_csv1, input_csv2, output_csv):
    reader1_list = list(csv.DictReader(open(input_csv1)))
    reader2_list = list(csv.DictReader(open(input_csv2)))

    with open(output_csv, mode='w', newline='') as outfile:
        fieldnames = ['Cross Section', 'Mean']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, row1 in enumerate(reader1_list):
            if i < len(reader2_list):
                writer.writerow({'Cross Section': row1['Cross Section'], 'Mean': reader2_list[i]['Mean']})
import csv

def sort_merged_csv(merged_csv_path):
    # Read the merged CSV file
    with open(merged_csv_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    # Sort the rows based on 'MJJMax'
    sorted_rows = sorted(rows, key=lambda x: float(x['Mean']))
    
    # Write the sorted rows back to the CSV file
    with open(merged_csv_path, mode='w', newline='') as outfile:
        fieldnames = sorted_rows[0].keys()  # Get the fieldnames from the first row
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_rows)

# Example usage within the main function or wherever needed
# sort_merged_csv('path/to/merged_output_sorted.csv')



import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_cross_sections_vs_mjj_with_global_uncertainties(csv_file_path_extracted, csv_file_path_real, csv_file_path_variance, csv_file_path_diff,label):
    dir_name = os.path.dirname(csv_file_path_extracted)
    label_dir = os.path.join(dir_name, label)
    os.makedirs(label_dir, exist_ok=True)
    
    plot_filename = os.path.basename(csv_file_path_extracted).replace('.csv', '.png')
    plot_filepath = os.path.join(label_dir, plot_filename)
    df_extracted = pd.read_csv(csv_file_path_extracted)
    df_real = pd.read_csv(csv_file_path_real)
    df_variance = pd.read_csv(csv_file_path_variance, skiprows=range(1), header=None, names=['Variance'])
    df_range = pd.read_csv(csv_file_path_diff)
    global_variance = float(df_variance.iloc[0]['Variance'])
    
    combined_df = pd.concat([df_extracted, df_real, df_variance], ignore_index=True)

    required_columns = ['Cross Section', 'value', 'Variance']
    missing_columns = [col for col in required_columns if col not in combined_df.columns]
    if missing_columns:
        raise ValueError(f"The following required columns are missing: {missing_columns}")
    
    fig, axs = plt.subplots(2, figsize=(10, 12))

    # First subplot: Cross Sections vs MJJMax with Global Uncertainties
    x = combined_df['Mean']
    y = combined_df['value']
    e = [global_variance] * len(combined_df)
    ex = [global_variance] * len(df_range)
    axs[0].set_xscale("linear")  # Set x-scale to linear
    axs[0].set_yscale("log")
    axs[0].errorbar(df_real['Mean'], df_real['value'], yerr=df_variance['Variance'], xerr=(df_range['Diff']), linestyle='None', marker='^', capsize=3, label=f'{label} Data with Global Uncertainties')
    axs[0].scatter(df_real['Mean'], (df_extracted['Cross Section']), c='red', alpha=0.6, label='Theoretical Predictions')
    
    axs[0].set_xlabel('MJJ [GeV]')
    axs[0].set_ylabel('Cross Section [pb]')
    axs[0].set_title(f'Cross Sections vs MJJMax with Global Uncertainties ({label})')
    axs[0].legend(loc='upper right')
    axs[0].grid(True)

    # Second subplot: Ratio of Cross Sections vs MJJMax
    axs[1].set_xscale
    axs[1].set_yscale
    axs[1].errorbar(df_real['Mean'], (df_real['value']/df_extracted['Cross Section']), linestyle='None', marker='^', capsize=3, label="Ratio")
    axs[1].set_xlabel('MJJ [GeV]')
    axs[1].set_ylabel('Ratio')
    axs[1].set_ylim(0.8,1.4)
    axs[1].set_title(f'Ratio: data/theory ({label})')
    axs[1].legend(loc='upper right')
    axs[1].grid(True)

    for index, row in df_extracted.iterrows():
        # Fetch the corresponding 'value' from df_real for each row in df_extracted
        real_row = df_real.loc[df_extracted['Mean'] == row['Mean']]
        if not real_row.empty:
            ratio = (real_row['value'].values[0]/row['Cross Section'])
            axs[0].annotate(f"{ratio:.2f}", (real_row['Mean'], real_row['value']), textcoords="offset points", xytext=(0,10), ha='center')
            print(ratio)
        else:
            print(f"No matching 'MJJ' found in df_real for {row['Mean']}")


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(plot_filepath, dpi=300, bbox_inches='tight')
    plt.show()


def save_and_plot_ratio(csv_file_path_extracted, csv_file_path_real, csv_file_path_variance, label):
    df_extracted = pd.read_csv(csv_file_path_extracted)
    df_real = pd.read_csv(csv_file_path_real)
    df_variance = pd.read_csv(csv_file_path_variance, skiprows=range(1), header=None, names=['Variance'])
    
    global_variance = float(df_variance.iloc[0]['Variance'])
    
    # Calculate the ratio
    df_extracted['ratio'] = df_real['value'] / df_extracted['Cross Section']
    
    # Save the ratio to a CSV file
    ratio_csv_path = f"{os.path.dirname(csv_file_path_extracted)}/{label}_ratio.csv"
    df_extracted.to_csv(ratio_csv_path, index=False)
    
    # Call the original plotting function with the calculated ratio
    #plot_cross_sections_vs_mjj_with_global_uncertainties(csv_file_path_extracted, csv_file_path_real, csv_file_path_variance, label)

def plot_correlation(csv_file_path, label):
    dir_name = os.path.dirname(csv_file_path)
    label_dir = os.path.join(dir_name, label)
    os.makedirs(label_dir, exist_ok=True)  # Create the directory if it doesn't exist
    
    correlation_filename = os.path.basename(csv_file_path).replace('.csv', '_correlation.png')
    correlation_filepath = os.path.join(label_dir, correlation_filename)
    
    df = pd.read_csv(csv_file_path)
    corr = df[['Cross Section', 'Mean']].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', cbar_kws={'label': 'Correlation'})
    plt.title(f'Correlation between Cross Section and MJJ ({label})')
    plt.xlabel('MJJMax')
    plt.ylabel('Cross Section')
    plt.savefig(correlation_filepath, dpi=300, bbox_inches='tight')
    plt.show()

def plot_table(csv_file_path_extracted, csv_file_path_real, csv_file_path_variance, csv_file_path_diff, label):
    plot_cross_sections_vs_mjj_with_global_uncertainties(csv_file_path_extracted, csv_file_path_real, csv_file_path_variance, csv_file_path_diff, label)
    save_and_plot_ratio(csv_file_path_extracted, csv_file_path_real, csv_file_path_variance, label)
    plot_correlation(csv_file_path_extracted, label)
'''
def process_directory(directory):
    
    label = None
    if "Table7" in directory:
        label = "0.0<y*<0.5"
    elif "Table8" in directory:
        label = "0.5<y*<1.0"
    elif "Table9" in directory:
        label = "1.0<y*<1.5"
    elif "Table10" in directory:
        label = "1.5<y*<2.0"
    elif "Table11" in directory:
        label = "2.0<y*<2.5"
    elif "Table12" in directory:
        label = "2.5<y*<3.0"
        
    csv_file_path_cross_section_extracted = f"{directory}/cross_section_output.csv"
    csv_file_path_output = f"{directory}/cross_section_output_sorted.csv"
    csv_file_path_mjjmax_extracted = f"{directory}/mjjmax_output.csv"
    csv_file_path_mjjmin_extracted = f"{directory}/mjjmin_output.csv"
    csv_file_path_mean_extracted = f"{directory}/MJJMean_NEW_NEW_NEW{label}.csv"
    csv_file_path_diff_extracted = f"{directory}/MJJDiff_NEW_NEW_NEW{label}.csv"
    merged_csv_path_extracted = f"{directory}/merged_output_sorted_NEW.csv"
    merged = f"{directory}/merged_output_sorted_Mark.csv"
    csv_file_path_real = f"{directory}/mergedHighLow_NEW_NEW_NEW{label}.csv"
    csv_file_path_variance = f"{directory}/varianceNewTable{directory.split('/')[-1]}.csv"
    csv_file_path_cross_delta_extracted = f"{directory}/CrossSections_DeltaMjj_DeltaY_NEW_NEW_NEW{label}.csv"
    
    #extract_cross_sections_and_save_csv([directory], csv_file_path_cross_section_extracted)
    sort_cross_section_csv(csv_file_path_cross_section_extracted, csv_file_path_output)
    #extract_mjjmax_values_and_save_csv([directory], csv_file_path_mjjmax_extracted)
    #extract_mjjmin_values_and_save_csv([directory], csv_file_path_mjjmin_extracted)
    #save_mjj_mean_values(csv_file_path_mean_extracted, label, csv_file_path_mjjmin_extracted, csv_file_path_mjjmax_extracted)
    #save_crosssection_deltamjj_deltay_values(csv_file_path_cross_delta_extracted, label, csv_file_path_cross_section_extracted, csv_file_path_diff_extracted)
    #merge_csv_files(csv_file_path_cross_delta_extracted, csv_file_path_mean_extracted, merged_csv_path_extracted)
    #sort_merged_csv(merged_csv_path_extracted)
    '''
    label = None
    if "Table7" in directory:
        label = "0.0<y*<0.5"
    elif "Table8" in directory:
        label = "0.5<y*<1.0"
    elif "Table9" in directory:
        label = "1.0<y*<1.5"
    elif "Table10" in directory:
        label = "1.5<y*<2.0"
    elif "Table11" in directory:
        label = "2.0<y*<2.5"
    elif "Table12" in directory:
        label = "2.5<y*<3.0"
    '''   
    #plot_table(merged_csv_path_extracted, csv_file_path_real, csv_file_path_variance, csv_file_path_diff_extracted, label)
    # Calculate and save ratios to a CSV file in the output directory
    #save_and_plot_ratio(merged_csv_path_extracted, csv_file_path_real, csv_file_path_variance, label)
    
    # Read the saved ratio CSV file
    #ratio_df = pd.read_csv(os.path.join(directory, f"{label}_ratio.csv"))

def main():
    output_dirs = [
        "/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_2/Table7",
        "/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_2/Table8",
        "/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_2/Table9",
        "/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_2/Table10",
        "/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_2/Table11",
        "/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_1_NP_2_eq_2/Table12",
    ]
    
    for directory in output_dirs:
        process_directory(directory)

if __name__ == "__main__":
    main()
