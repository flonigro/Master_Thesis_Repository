import os
import yaml
import csv
import numpy as np
import pandas as pd

directory = '/home/turing/MG5_aMC_v3_4_2/dijet/data/rawdata/CMS_2JET_7TEV_rawdata/'
labels = ["0.0<y*<0.5", "0.5<y*<1.0", "1.0<y*<1.5", "1.5<y*<2.0", "2.0<y*<2.5"]
output_base_dir = '/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0'

def extract_errors_from_yaml(yaml_file_path):                                 
    with open(yaml_file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    
    errors_by_value = {}
    for dependent_variable in yaml_content.get('dependent_variables', []):
        for value in dependent_variable.get('values', []):
            value_key = value.get('value')
            if value_key is not None:
                if value_key not in errors_by_value:
                    errors_by_value[value_key] = []
                for error in value.get('errors', []):
                    # Skip processing if the error is a statistical error ('stat')
                    #if 'symerror' in error and 'stat' in error.get('label', ''):
                    #    continue
                    if 'symerror' in error:
                        errors_by_value[value_key].append(float(error['symerror']))
                    elif 'asymerror' in error:
                        asym_error_minus = -float(error['asymerror']['minus'])
                        asym_error_plus = float(error['asymerror']['plus'])
                        semi_value = (asym_error_plus +  asym_error_minus) * 0.5
                        average = (asym_error_plus - asym_error_minus) * 0.5
                        errors_by_value[value_key].append(np.sqrt(average**2 + 2*(semi_value)**2))
                        
    return errors_by_value

def write_errors_and_variances_to_csv(errors_by_value, table_number):
    # Construct the output file paths using the table_number
    errors_output_file_path = f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/{table_number}/errNew_file.csv"
    variance_output_file_path = f"/home/turing/MG5_aMC_v3_4_2/CMS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/{table_number}/varianceNewTable{table_number}.csv"
    
    write_errors_to_csv(errors_by_value, errors_output_file_path)
    write_variances_to_csv(calculate_variance(list(errors_by_value.values())), variance_output_file_path)

def write_errors_to_csv(errors_by_value, output_file_path):
    with open(output_file_path, mode='w', newline='') as csvfile:
        fieldnames = ['Type', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for value_key, errors in errors_by_value.items():
            for error in errors:
                writer.writerow({'Type': 'SymError', 'Value': str(error)})
            print(f"\nSum in quadrature (Variance) for Value {value_key}: {np.sqrt(np.sum([e**2 for e in errors]))}")

def write_variances_to_csv(variances, output_file_path):
    with open(output_file_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["variance"])
        for variance in variances:
            writer.writerow([variance])

def calculate_variance(errors_list):
    variances = []
    for errors in errors_list:
        mean_error = np.mean(errors)
        variance = np.sum([(e - mean_error) ** 2 for e in errors]) / len(errors_list)
        variances.append(np.sqrt(variance))
    return variances

def process_yaml_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.yaml'):
            file_path = os.path.join(directory_path, filename)
            # Adjusted logic to correctly extract the table number
            table_number = int(filename.split('-v1-Table_')[1].split('.')[0])
            errors_by_value = extract_errors_from_yaml(file_path)
            # Corrected the call to pass the correct parameters
            write_errors_and_variances_to_csv(errors_by_value, f"Table{table_number}")
            
def extract_dependent_variable_values(data, prefix=''):
    if 'dependent_variables' in data:
        for i, item in enumerate(data['dependent_variables']):
            if 'values' in item:
                for j, value_item in enumerate(item['values']):
                    if 'value' in value_item:
                        yield (prefix + '.' + str(j+1) if prefix else str(j+1), value_item['value'])
                    if 'errors' in value_item:
                        for error in value_item['errors']:
                            if 'value' in error:
                                yield (prefix + '.' + str(j+1) + '.errors.' + error['label'] if prefix else str(j+1) + '.errors.' + error['label'], error['value'])       
        
def extract_high_values(data):
    if 'independent_variables' in data:
        for var in data['independent_variables']:
            if 'values' in var:
                for value_item in var['values']:
                    if 'high' in value_item:
                        yield (var['header']['name'], value_item['high'])

def save_mjj_high_values(table_number, label, high_values):
    table_directory = os.path.join(output_base_dir, f'Table{table_number}')
    if not os.path.exists(table_directory):
        os.makedirs(table_directory)
    
    file_name = f'MJJHighValues_NEW_NEW_NEW{label}.csv'
    file_path = os.path.join(table_directory, file_name)
    
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['High']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, high_value in high_values:
            adjusted_high_value = high_value
            writer.writerow({'High': adjusted_high_value})
            
def extract_low_values(data):
    if 'independent_variables' in data:
        for var in data['independent_variables']:
            if 'values' in var:
                for value_item in var['values']:
                    if 'high' in value_item:
                        yield (var['header']['name'], value_item['low'])

def save_mjj_low_values(table_number, label, low_values):
    table_directory = os.path.join(output_base_dir, f'Table{table_number}')
    if not os.path.exists(table_directory):
        os.makedirs(table_directory)
    
    file_name = f'MJJLowValues_NEW_NEW_NEW{label}.csv'
    file_path = os.path.join(table_directory, file_name)
    
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Low']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name, low_value in low_values:
            adjusted_low_value = low_value
            writer.writerow({'Low': adjusted_low_value})
        

def merge_values_low_with_high_mjj(input_high_values_csv, input_low_values_csv, output_csv):
    """
    Merges valuesReal CSV files and MJJHigh values for every output directory in a separate CSV file with the corresponding label,
    merging the high and low values into one column and sorting them from highest to lowest.
    """
    high_values_reader_list = list(csv.DictReader(open(input_high_values_csv)))
    low_values_reader_list = list(csv.DictReader(open(input_low_values_csv)))

    # Combine high and low values into one list
    combined_values = []
    for high_row, low_row in zip(high_values_reader_list, low_values_reader_list):
        combined_values.append(float(high_row['High']) + float(low_row['Low']))

    # Sort the combined values from highest to lowest
    sorted_values = sorted(combined_values, reverse=True)

    # Write the sorted values to the output CSV file
    with open(output_csv, mode='w', newline='') as outfile:
        fieldnames = ['Sorted Values']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for value in sorted_values:
            writer.writerow({'Sorted Values': value})
            
def save_mjj_mean_values(table_number, label, input_mjj_low_csv, input_mjj_high_csv):
    table_directory = os.path.join(output_base_dir, f'Table{table_number}')
    if not os.path.exists(table_directory):
        os.makedirs(table_directory)
    
    file_name = f'MJJMean_NEW_NEW_NEW{label}.csv'
    file_path = os.path.join(table_directory, file_name)

    mjj_low_df = pd.read_csv(input_mjj_low_csv)
    mjj_high_df = pd.read_csv(input_mjj_high_csv)

    mean_df = (mjj_low_df['Low'] + mjj_high_df['High']) / 2
    mean_df = pd.DataFrame(mean_df, columns=['Mean'])

    mean_df.to_csv(file_path, index=False)


    
def save_mjj_diff_values(table_number, label, input_mjj_low_csv, input_mjj_high_csv):
    table_directory = os.path.join(output_base_dir, f'Table{table_number}')
    if not os.path.exists(table_directory):
        os.makedirs(table_directory)
    
    file_name = f'MJJDiff_NEW_NEW_NEW{label}.csv'
    file_path = os.path.join(table_directory, file_name)

    mjj_low_df = pd.read_csv(input_mjj_low_csv)
    mjj_high_df = pd.read_csv(input_mjj_high_csv)

    # Ensure both DataFrames have the same structure and columns
    #assert set(mjj_low_df.columns) == set(mjj_high_df.columns), "DataFrames have different columns"

    # Calculate the mean between corresponding rows from both DataFrames
    # Assuming the columns to take the mean of are named 'ColumnToTakeMeanOf'
    # Replace 'ColumnToTakeMeanOf' with the actual column name(s) you want to average
        
    mean_df = ((mjj_high_df['High'] - mjj_low_df['Low'])*0.5)

    mean_df = pd.DataFrame(mean_df, columns=['Diff'])

    # Write the calculated means to a new CSV file
    mean_df.to_csv(file_path, index=False)

def merge_values_real_with_mean_mjj(input_values_real_csv, input_mjj_mean_csv, output_csv):
    """
    Merges valuesReal CSV files and MJJHigh values for every output directory in a separate CSV file with the corresponding label.
    """
    values_real_reader_list = list(csv.DictReader(open(input_values_real_csv)))
    mjj_mean_reader_list = list(csv.DictReader(open(input_mjj_mean_csv)))

    with open(output_csv, mode='w', newline='') as outfile:
        fieldnames = ['value', 'Mean']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, row_real in enumerate(values_real_reader_list):
            if i < len(mjj_mean_reader_list):
                writer.writerow({'value': row_real['value'], 'Mean': mjj_mean_reader_list[i]['Mean']})


# Modified main function...
def main():
    for table_number in range(6, 11):
        table_directory = os.path.join(output_base_dir, f'Table{table_number}')
        if not os.path.exists(table_directory):
            os.makedirs(table_directory)
        
        label = labels[table_number - 6]
        file_path = os.path.join(table_directory, f'valuesReal_NEW_NEW_NEW{label}.csv')
        table_values = []
        high_values = []
        low_values = []

        file_path_yaml = os.path.join(directory, f'HEPData-ins1208923-v1-Table_{table_number}.yaml')
        
        try:
            with open(file_path_yaml, 'r') as file:
                data = yaml.safe_load(file)

            for _, value in extract_dependent_variable_values(data):
                table_values.append({'value': value})
            
            high_values = [(var['header']['name'], value_item['high']) for var in data.get('independent_variables', []) for value_item in var.get('values', []) if 'high' in value_item]
            low_values = [(var['header']['name'], value_item['low']) for var in data.get('independent_variables', []) for value_item in var.get('values', []) if 'low' in value_item]
            save_mjj_high_values(table_number, label, high_values)
            #save_mjj_high_values_in_an_other_file(table_number, label, high_values)
            save_mjj_low_values(table_number, label, low_values)
            #save_mjj_low_values_in_an_other_file(table_number, label, low_values)
            
            errors_by_value = extract_errors_from_yaml(file_path_yaml)
            write_errors_and_variances_to_csv(errors_by_value, f"Table{table_number}")
        except FileNotFoundError:
            print(f"File {file_path_yaml} not found.")

        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in table_values:
                writer.writerow(entry)

        # New integration: Call merge_values_real_and_mjj_high after processing each YAML file
        file_path_values_real = os.path.join(table_directory, f'valuesReal_NEW_NEW_NEW{label}.csv')
        file_path_mjj_high = os.path.join(table_directory, f'MJJHighValues_NEW_NEW_NEW{label}.csv')
        file_path_mjj_low = os.path.join(table_directory, f'MJJLowValues_NEW_NEW_NEW{label}.csv')
        file_path_mjj_mean = os.path.join(table_directory, f'MJJMean_NEW_NEW_NEW{label}.csv')
        output_file_path = os.path.join(table_directory, f'mergedHighLow_NEW_NEW_NEW{label}.csv')
        #output_file_path_1 = os.path.join(table_directory, f'merged_Low_Hih{label}.csv')
        save_mjj_mean_values(table_number, label, file_path_mjj_low, file_path_mjj_high)
        #save_mjj_mean_values_in_an_other_file(table_number, label, file_path_mjj_low, file_path_mjj_high)
        save_mjj_diff_values(table_number, label, file_path_mjj_low, file_path_mjj_high)
        merge_values_real_with_mean_mjj(file_path_values_real, file_path_mjj_mean, output_file_path)
        #merge_values_low_with_high_mjj(file_path_mjj_high, file_path_mjj_low, output_file_path)

if __name__ == '__main__':
    main()
