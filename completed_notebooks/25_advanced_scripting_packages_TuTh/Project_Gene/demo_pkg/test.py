#!/opt/anaconda3/bin/python

import sys
import numpy as np

test_variable = 40


print("This is a python script")

def test_function(no = 0):
    print("This is a function in a python script")
    return no + 1

def say_hi(name = "class BIOINF 575"):
    print(len(name))
    return f"hi {name}"

def main():
    test_variable = 10
    print(f'The test variable value is {test_variable}')

print(f"name variable is {__name__}")

if __name__ == "__main__":
    # execute only if run as a script
    print('Number of arguments:', len(sys.argv))
    print ('Argument List:', str(sys.argv))
    string_list = sys.argv[1]
    test_array = np.array(string_list.strip('][').split(','), dtype = int)
    print(f"the array is {test_array * int(sys.argv[3])}")
    main() 