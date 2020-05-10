'''

Program: File Duplicate Finder and Remover
Author: Vignesh Natarajan (www.vikilabs.in)

'''

import os

import os
import re
import csv
import filecmp
from os.path import join, getsize

DEBUG=False
indexed_files = {}


csv_file_name="/Users/viki/Downloads/test.csv"

def init_csv(csv_file_name):
    with open(csv_file_name, "w") as file:
        print "CSV INITIALIZED"

def write_csv(csv_file_name, row):
    with open(csv_file_name, "a") as file:
        writer = csv.writer(file, delimiter=',')
        row.insert(0, "DUPLICATE FILES")
        writer.writerow(row)

def parse_file_name(file_name_with_path):
    flist = file_name_with_path.split("/")
    file_name = flist[len(flist) - 1]
    return file_name

def get_file_extension_list(file_extensions):
    elist = file_extensions.split(",")
    elist_new = []
    for i in elist:
        f = i.strip()
        elist_new.append(f)
    return elist_new

def is_pattern_exist(main_string, pattern):
    return re.search(pattern, main_string)

def is_pattern_exist_ignore_case(main_string, pattern):
    return re.search(pattern, main_string, re.IGNORECASE)

def index_file(file_size, file_name):
    key = file_size

    if key in indexed_files:
        if DEBUG:
            print "INSERT : ", file_name
        indexed_files[key].append(file_name)
    else:
        indexed_files[key] = []
        if DEBUG:
            print "APPEND : ", file_name
        indexed_files[key].append(file_name)

'''
   file_extensions = Should be comma seperated [Ex: .jpeg, .gif]
'''



def get_all_files(search_path, file_extensions):

    if file_extensions:
        extension_list = get_file_extension_list(file_extensions)

    for path, dirs, files in os.walk(search_path):
        for file in files:
            file_name_with_path = os.path.join(path,file)

            if not os.path.exists(file_name_with_path):
                continue

            fstat = os.stat(file_name_with_path)
            file_size = int(fstat.st_size)
            if file_extensions:
                for e in extension_list:
                    if is_pattern_exist(file_name_with_path, e):
                        index_file(file_size, file_name_with_path)
            else:
                index_file(file_size, file_name_with_path)

            if DEBUG:
                print file_size, file_name_with_path

def traverse_dulicate_files():
    keylist = indexed_files.keys()
    keylist.sort()

    for key in keylist:
        prev_file = ""
        for file in indexed_files[key]:
            if prev_file:
                if filecmp.cmp(prev_file, file):
                    print "DUPLICATE FOUND [ "+prev_file+" ] and [ "+file+" ]"
            prev_file = file

def find_duplicates():
    keylist = indexed_files.keys()
    keylist.sort()

    for key in keylist:
        prev_file = ""
        duplicates = []
        for file in indexed_files[key]:
            duplicates = []
            if prev_file:

                if filecmp.cmp(prev_file, file):
                    print "DUPLICATE FOUND [ " + prev_file + " ] and [ " + file + " ]"
                    if prev_file not in duplicates:
                        duplicates.append(parse_file_name(prev_file))
                    if file not in duplicates:
                        duplicates.append(parse_file_name(file))

            prev_file = file
        if duplicates:
            write_csv(csv_file_name, duplicates)



def delete_duplicates():
    keylist = indexed_files.keys()
    keylist.sort()

    for key in keylist:
        prev_file = ""
        for file in indexed_files[key]:
            if prev_file:
                if filecmp.cmp(prev_file, file):
                    print "DUPLICATE FOUND [ " + prev_file + " ] and [ " + file + " ]"
                    print "DELETING [ "+prev_file+" ]"
                    os.remove(prev_file)
            prev_file = file

init_csv(csv_file_name)
get_all_files("/Users/viki/", ".jpg, .pdf, .mp4, .jpeg, .mkv, .mp3, .m4v")
find_duplicates()
