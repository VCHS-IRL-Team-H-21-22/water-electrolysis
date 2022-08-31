import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from scipy.optimize import curve_fit

import csv
import glob
import os
import sys

################################
# Usage: python3 analyze.py {dataset}
#
# {dataset} = 'flight' or 'ground'
# 
# Obtain the current readings in each camera txt file located in ./data/
# and convert them to hex and display them in milliamps.
################################

def exponential(x, A, B,C):
    y = A*np.exp(-1*B*x)+C
    return y

pause_times = [0.5,1, 1.5, 3, 8]
index = 0

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = f'{script_dir}/{sys.argv[1]}_data/'

output = csv.writer(open(f'{script_dir}/analyze_{sys.argv[1]}.csv', 'w+', newline=''))
output.writerow(['name', 'A', 'B', 'C', 'A_err', 'B_err', 'C_err', 'r_squared'])

files = sorted(glob.glob(f'{data_dir}/*.TXT'))

prefix = 'f' if sys.argv[1]=='flight' else 'g'
trial_num = 0

for file in files:
    with open(file, 'r') as fr:
        if pause_times[index] != max(pause_times):
            index +=1
            continue
        trial_num += 1
        lines = fr.readlines()
        file_name = file[file.rfind('/') + 1 :]
        print(
            '\n==================  '
            +  file_name # name of the text file
            + '  =================='
        )

        data = [int(x,16)/10 for x in lines[17][:-2].split()] # convert from HEX to DEC
        data.pop(0) # first element is always FFFF

        ## Time and readings
        print(lines[2])
        print(data)
        
        ## Display graph
        x = []  # time
        for i in range(len(data)):
            x.append( i * pause_times[index])
        index = (index+1)%len(pause_times)

        x.pop(0) # Ignore first element since is always zero
        data.pop(0)
        data_err = np.zeros(len(data)) + 0.05
        print(data_err)
        

        ## Fit graph to exponential
        parameters, covariance = curve_fit(exponential, x, data, sigma=data_err, absolute_sigma=True, maxfev=5000)
        A = parameters[0]
        B = parameters[1]
        C = parameters[2]
        parameter_error = np.sqrt(np.diag(covariance)) # https://micropore.wordpress.com/2017/02/04/python-fit-with-error-on-y-axis/
        A_err = parameter_error[0]
        B_err = parameter_error[1]
        C_err = parameter_error[2]
        fit = exponential(np.array(x), A, B,C)
        print(parameters)
        print(covariance)
        ## Calculate stats
        residuals = data - fit
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((data-np.mean(data))**2)
        r_squared = 1 - (ss_res / ss_tot)

        print('Fitted values for exponential y=A exp (-Bx) + C:')
        print('Using σ = 0.05 for all the data')
        print('A: ' + str(A), '+ or -', str(A_err))
        print('B: ' + str(B), '+ or -', str(B_err))
        print('C: ' + str(C), '+ or -', str(C_err))  
        print('R^2=' + str(r_squared))
        output.writerow([file_name, A, B, C, A_err, B_err, C_err, r_squared] + data)
        
        plt.figure(figsize=(10.666, 6))
        rc('font',**{'family':'serif','serif':['Arial'],'size':14})
        #rc('text', usetex=True)
        plt.errorbar(x, data, fmt='o', yerr = data_err, label='data')
        plt.plot(x, fit, '-', label=f'fit: y = A exp(-Bx) + C\nA={round(A,4)}\nB={"%.4f" % round(B,4)}\nC={round(C,4)}')

        plt.legend(title=f'R²={round(r_squared, 3)}')
        plt.title(f'Trial {prefix}{trial_num}')
        plt.ylabel('Current reading (mA)')
        plt.xlabel('Time after turning on electrolysis (s)')
        plt.show()




