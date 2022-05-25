import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import glob

################################
# Usage: python3 analyze.py
#
# No arguments
# 
# Obtain the current readings in each camera txt file located in ./data/
# and convert them to hex and display them in milliamps.
################################

def exponential(x, A, B,C):
    y = A*np.exp(-1*B*x)+C
    return y

pause_times = [0.5,1, 1.5, 3, 8]
index = 0

data_dir = "./data/"
files = glob.glob(data_dir + "*.TXT")
files.sort()
for file in files:
    with open(file, "r") as fr:
        lines = fr.readlines()
        print(
            "\n==================  "
            + file[file.rfind("/") + 1 :] # name of the text file
            + "  =================="
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

        # plt.scatter(x, data)
        # plt.ylabel('Current reading (mA)')
        # plt.xlabel('Time after turning on electrolysis (s)')
        # plt.show()

        ## Fit graph to Gaussian
        parameters, covariance = curve_fit(exponential, x, data)
        A = parameters[0]
        B = parameters[1]
        C = parameters[2]
        fit = exponential(np.array(x), A, B,C)

        print("Fitted values for exponential y=A exp (-Bx) + C:")
        print("A: " + str(A))
        print("B: " + str(B))
        print("C: " + str(C))
        
        plt.plot(x, data, 'o', label='data')
        plt.plot(x, fit, '-', label='fit: y= ' +str(round(A,1))+' exp(-'+str(round(B,1))+'x) + '+str(round(C,1)))
        plt.legend()
        plt.ylabel('Current reading (mA)')
        plt.xlabel('Time after turning on electrolysis (s)')
        plt.show()




