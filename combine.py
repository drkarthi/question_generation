import subprocess
import sys

filename = sys.argv[1]
str1 = sys.argv[2]
str2 = sys.argv[3]
output = subprocess.check_output(['python', 'parse.py', filename, str1, str2])[:-1]
input2 = ''.join( output[1:-1].split(',') )
input2 = input2.replace("\'","")
output2 = subprocess.check_output(['python', 'rst_ordering.py', input2])
print output2.strip('\n')