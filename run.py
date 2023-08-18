# author: Mohamad Mahdi Reisi
# Date: 2023/8/16

# Description: This file is used to run the main.py file
# the reason for this file is that we want to run the main.py file from the root directory of the project
# so we can use the relative path to import the modules


import os 

file_path = os.path.abspath(__file__).split('run.py')[0]

# go to the file path address
os.chdir(file_path)


different_python_name_in_terminal = ['python3', 'python', 'py']

# run the main.py file
flag = False
for i in different_python_name_in_terminal:
    try:
        os.system(i + ' src/main.py')
        flag = True
        break
    except:
        continue

if not flag:
    print('Error: python is not installed on your system or you have not added it to the path')
