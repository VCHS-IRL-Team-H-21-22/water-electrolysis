#!/usr/bin/python3

import matplotlib.pyplot as plt

import glob

################################
# Usage: ./CameraFileScraper
#
# No arguments
# 
# Obtain the current readings in each camera txt file
# and convert them to hex and display them in milliamps.
################################

pause_times = [0.5,1, 1.5, 3, 8]
index = 0

data_dir = "./data/"
for file in glob.glob(data_dir + "*.TXT"):
    with open(file, "r") as fr:
        lines = fr.readlines()
        print(
            "\n==================  "
            + file[file.rfind("/") + 1 :]
            + "  =================="
        )
        print(lines[2])
        data = [int(x,16)/10 for x in lines[17][:-2].split()]
        data.pop(0) # first element is always FFFF
        print(data)
        
        x = [] #times
        for i in range(len(data)):
            x.append( i * pause_times[index])
        index = (index+1)%len(pause_times)
        plt.scatter(x, data)
        plt.show()
