#!/usr/bin/python3

import glob

################################
# Usage: ./CameraFileScraper
#
# No arguments
# Obtain the current readings in each camera txt file
# and convert them to hex and display them in milliamps.
# TODO: Make plot based on time
################################

data_dir = "./data/"
for file in glob.glob(data_dir + "*.TXT"):
    with open(file, "r") as fr:
        lines = fr.readlines()
        print(
            "\n==================  "
            + file[file.rfind("/") + 1 :]
            + "  =================="
        )
        print(lines[17][:-2])
        print([int(str(x), 16) / 10 for x in lines[17][:-2].split()])
