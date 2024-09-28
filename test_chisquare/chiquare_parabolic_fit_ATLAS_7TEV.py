#Script to generale CHisquare fit vs Otg
#The goal is to find the range of Otg values in which the Xsquare is minimized/ where the DeltaX^2 = 1
#For this, T(c) = SM + c*LIN + c^2*QUAD
#x^2 = (D - T(c))^T @ covmat^-1 @ (D - T(c)), where D are central hep data points and covmat is the covariance matrix  of hepdata points
import numpy as np
from numpy import correlate
import pandas as pd
import os
from numpy.polynomial import polynomial
import csv
from itertools import combinations
from numpy.linalg import inv
from scipy.optimize import minimize
import yaml
import matplotlib.pyplot as plt  
from matplotlib.figure import Figure 
import numpy as np  

c_values = np.linspace(-3,3,50) 

#Calculate ChiSquare

def calculate_chi2(sm_extracted, sm_real, smeft_linear, smeft_quadratic, c, cov_matrix):
    data = sm_real['value'].values

    diff = ((sm_real['value'] - ((sm_extracted['Cross Section'] + c *( smeft_linear['Cross Section']) + c*c*((smeft_quadratic['Values'])).T))) @ (np.abs(cov_matrix)) @ (sm_real['value'] - (sm_extracted['Cross Section'] + c * (smeft_linear['Cross Section']) + c*c*(smeft_quadratic['Values'])))/len(data-1))
    #print("invcov", inv_cov_matrix)

    #print("diff", diff)
    return diff

#We want to find values of c, in the given rangem which minimize ChiSquare, so we ask that the difference among chi2 value and the lowest values is 1.
def find_near_one_chi2(chi2_values, tolerance=380):
    """
    :param chi2_values: List of chi2 values calculated for different c values.
    :param tolerance: Tolerance level for considering a DeltaChiSquare value close to 1.
    """
    min_abs_chi2 = min(chi for chi in chi2_values)
    print("MINIMO with", min_abs_chi2)
    for i, chi2 in enumerate(chi2_values):
        if (chi2 == min_abs_chi2 ):
            print(f"C value close to 1: {c_values[i]:.2f} with chi2 value: {min_abs_chi2:.2f}")
        else:
            print(f"Change tolerance")
import seaborn as sns

def plot_heatmap(y):
    """
    Plots a heatmap of the covariance matrix.
    
    Parameters:
    - cov_matrix: A 2D numpy array representing the covariance matrix.
    """
    plt.figure(figsize=(10, 8))  # Set figure size
    sns.heatmap(y, annot=False, cmap="RdYlBu")  # Create heatmap
    plt.title('Covariance Matrix Heatmap')  # Set title
    plt.xlabel('Bins')  # Label x-axis
    plt.ylabel('Bins')  # Label y-axis
    plt.show()  # Display the plot




def main():
    #dealing with files and directories
    
    for table_number in range(7, 13):
        label = ["0.0_y__0.5", "0.5_y__1.0", "1.0_y__1.5", "1.5_y__2.0", "2.0_y__2.5", "2.5_y__3.0"][table_number - 7]
        directory = '/home/turing/MG5_aMC_v3_4_2/dijet/data/rawdata/ATLAS_2JET_7TEV_R06_rawdata/'
    
        output_base_dir = "/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/"
        
        table_directory = os.path.join(output_base_dir, f'Table{table_number}')
        if not os.path.exists(table_directory):
            os.makedirs(table_directory)

        #defining directories csv files
        
        sm_extracted_path = os.path.join(output_base_dir, 'combined_data_sm_extracted.csv')
        sm_real_path = os.path.join(output_base_dir, f'combined_data_sm_real.csv')
        smeft_linear_path = f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/combined_data_smeft_lin_.csv"
        smeft_quadratic_path = f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/combined_data_smeft_quad_.csv"
        cov_mat=f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/inverse_result_matrix.csv"
        #covariance = f"/home/turing/MG5_aMC_v3_4_2/ATLAS_DIJET_7TEV_SCRIPTS_CG_0_NP_eq_0/COV_MAT_ATLAS_DIJET_7TEV_new_new.csv"
        sm_real = pd.read_csv(sm_real_path)
        sm_extracted = pd.read_csv(sm_extracted_path)
        smeft_linear = pd.read_csv(smeft_linear_path)
        smeft_quadratic = pd.read_csv(smeft_quadratic_path)
        cov_mat_df = pd.read_csv(cov_mat)
        #covariance_df = pd.read_csv(covariance)
        cov_matt = cov_mat_df.values
        #call of ChiSquare
        #covariance_matrix(cov_mat)
        chi2 = []
        #plot_heatmap(cov_matt)
        data = {'c': [], 'chi2': []}

        for c in c_values:
            chi2_value = calculate_chi2(sm_extracted, sm_real, smeft_linear, smeft_quadratic, c, cov_matt)
            #print("c", c, "and chi", chi2_value)
            chi2.append(chi2_value)
            find_near_one_chi2(chi2, tolerance=1)
    
            # Append the current c and chi2 values to the DataFrame
            data['c'].append(c)
            data['chi2'].append(chi2_value)

            # Convert the DataFrame to a CSV file
            df = pd.DataFrame(data)
            df.to_csv('/home/turing/MG5_aMC_v3_4_2/c_vs_chi2.csv', index=False)
        
            #sns.pairplot(df, vars=['c', 'chi2'], diag_kind='kde')

            # Show the plot
            #plt.show()
        #datas = sns.load_dataset("df")
        #sns.pairplot(df)
        g = sns.pairplot(df, diag_kind="kde")
        g.map_lower(sns.kdeplot, levels=4, color=".2")
        #sns.pairplot(df, vars=['c', 'chi2'], diag_kind='kde')
        #sns.heatmap(df.corr())
        plt.show()
        
        #write chisquare values in an array for plot    
        y = np.array(chi2)
        #x_fit = np.arange(-5, 6, 1)
        x_fit = np.linspace(min(c_values), max(c_values), 50)  # Generate x values for the fit
        #y_fit = polynomial(x_fit)
        #sns.heatmap((x_fit, y))#PLOT of chisquare vs c values
        #plt.figure(figsize=(10, 6))
        try:
            
            coefficients = np.polyfit(c_values, y, 4)  # Fit a second-degree polynomial
            polynomial = np.poly1d(coefficients)
           
            # Find x-values where the fitted function equals 1
            min_abs_chi2 = min(chi for chi in y)
            val = abs(27.90 - min_abs_chi2)
            intersection_x_values = np.roots(polynomial - 27.90)
            intersection_x_values = intersection_x_values.real  # Take real part since roots might be complex
            print("Otg Values:", intersection_x_values)
    
            # Filter out invalid solutions (e.g., NaN due to numerical instability)
            valid_intersection_indices = ~np.isnan(intersection_x_values)
            intersection_x_values = intersection_x_values[valid_intersection_indices]
    
            # Plotting the fitted quadratic function
            x_fit = np.linspace(min(c_values), max(c_values), 50)  # Generate x values for the fit
            y_fit = polynomial(x_fit)  # Calculate y values for the fit
        
            # Plotting y_fit instead of y in a subplot
            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
            ax[0].plot(c_values, y, color='blue', label='X^2 with Formula')  # Original data in the left subplot
            ax[0].set_title('X^2 with Formula')
            #ax[0].set_ylim(138,140)
            #ax[0].set_xlim(-0.3,0.3)
    
            # Adding y = 1 line to the first subplot
            ax[0].plot(x_fit, (27.90)*np.ones_like(x_fit), 'r--', label='DeltaChi^2 = 1')  # Red dashed line representing y = 1
            
            # Highlighting intersections in the first subplot
            ax[0].scatter(intersection_x_values, (27.90)*np.ones_like(intersection_x_values), color='red', marker='o', s=50, zorder=10)
            #ax[0].set_ylim(1.0,1.5)
            ax[0].legend()
            
            ax[1].plot(x_fit, y_fit, color='green', linestyle='-', label='X^2 with fit Quadratic Function')  # Fitted function in the right subplot
            ax[1].set_title('X^2 with fit Quadratic Function')
        
            # Adding y = 1 line to the second subplot
            ax[1].plot(x_fit, 27.90*np.ones_like(x_fit), 'r--', label='y = 1')  # Red dashed line representing y = 1
            
            # Highlighting intersections in the second subplot
            ax[1].scatter(intersection_x_values, 27.90*np.ones_like(intersection_x_values), color='red', marker='o', s=50, zorder=10)
            
            ax[1].legend()
    
            plt.tight_layout()
            plt.savefig(os.path.join(table_directory, f'chi2_plot_Table{table_number}.png'))
            plt.show()

        except TypeError as e:
            #print(f"Error in np.polyfit: {e}")
            exit(1)  # Exit the script if there's an error
    
if __name__ == "__main__":
    main()
