# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to run the main.py file
# the reason for this file is that we want to run the main.py file from the root directory of the project
# so we can use the relative path to import the modules


import os 

file_path = os.path.abspath(__file__).split('run.py')[0]

# go to the file path address
os.chdir(file_path)


import src.main

