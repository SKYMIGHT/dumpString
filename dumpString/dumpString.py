#!/usr/bin/python3
# Confidential - Copyright 2021 Teradyne Inc
#
# This material contains certain trade secrets and confidential and
# proprietary information of Teradyne. Use, reproduction, disclosure,
# or distribution by any means are prohibited, except pursuant to a
# written license from Teradyne. Use of copyright notice is precautionary
# and does not imply publication or disclosure.
#
# Filename: dumpString.py
#
# Description:
#  - Find match string the dump to files 
# Modifications:
# Date         Owner             Short description
# 06/24/2021   David-Wei Huang        Initial version
#/////////////////////////////////////////////////////////////////////

import os, sys, getopt, re

# 1) Import datalog
# 2) Matching Fail site
# 3) Output list of tests with no match


datalog_path = ""

def print_error(e):
    if e == 0:
        print("usage: " + os.path.basename(__file__) + \
            "[ [[-l <Datalog_Path.txt>] | [-r <datalog_folder>]]]")
        sys.exit()

def main(argv):
    global datalog_path

    datalog_path = ""
    recursivepath = ""

    try:
        opts, args = getopt.getopt(argv,"h:l:r:")
    except getopt.GetoptError:
        print_error(0)
    
    for opt, arg in opts:
        if opt == '-h':
            print_error(0)
        elif opt == '-l':
            datalog_path = arg.lstrip()
        elif opt == '-r':
            recursivepath = arg.lstrip()
    
    if ( recursivepath == ''):
        print_error(0)


    
    # Process datalog
    if recursivepath != "":
        for(path, dirs, files) in os.walk(recursivepath):
            for f in files:
                if ".txt" in f and '.swp' not in f and '_mod' not in f:
                    datalog_path = os.path.join(path, f)
                    process_file()
    elif datalog_path != "":
        process_file()

def process_file():
    global datalog_path

    delimitor = '\t'

    TestName_col = -1
    PETestName_col = -1
    LoLim_col = -1
    HiLim_col = -1

    LSgroups = []
    TCMgroups = []

    FailLine = ''


    # Handle escape characters in Windows path
    datalog_path = datalog_path.replace('\n','\\n').replace('\r','\\r').replace('\t','\\t').replace('\b','\\b').replace('\f','\\f').replace('\\','/')

    print('-----')
    print('Datalog file is:\t\t', datalog_path)

    inputfile = os.path.basename(datalog_path)
    inputfile = inputfile.split('#')[0]
    inputfile = inputfile.split('.')[0]

    print('Output file is:\t\t', inputfile + "_mod.txt")

    try:
        fp = open(datalog_path,"r")
    except getopt.GetoptError:
        print_error(0)

    for line in fp.readlines():
        if 'Fail (F) : (X,Y) =' in line:
            #print (line)
            
            FailLine += line

    # Output new datalog 
    with open(inputfile + "_mod.txt", "w") as f:
        f.write(FailLine)



if __name__ == "__main__":
    main(sys.argv[1:])