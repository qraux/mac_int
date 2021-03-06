# Query Logic for Mounted Devices/Volumes v1.0
# Justin Boncaldo (@boncaldoj), Zachary Burnham (@zmbf0r3ns1cs) 2019
# ----------------------------------------------------------

import sqlite3
import os
import re
import json
from var_db import *

# Start of function called upon by Main Function (mac_int.py)
def mountedVolumesRun(output_dir, input_path, user_name):
    # Output file and DB specified in mac_int.py
    file = open(output_dir + "\\mac_int-MOUNTEDVOLUMES-" + user_name +"-Output.txt", 'w+')
    connection = sqlite3.connect(input_path)
    cursor = connection.cursor()

    # Username search (determined in mac_int.py)
    userSearch = user_name

    # Mounted Volume variables
    global a, b, i, output

    volLength = 0

    # Define lists
    d = []
    e = []

    # Define counters for list positions
    y = 0 # volList list position
    counter = 0

    end = "no" # Runs while loop (EVERYTHING)
    output = None

    # Define variables for table
    while end != "yes":
        if (counter == 0) or (counter == 1):
            # Define Volume Name List Variables
            if counter == 0:
                print("[~] Finding Volumes for " + str(userSearch) + "...")
                a = n
                b = ri
            # Define Created Date List Variables
            elif counter == 1:
                print("[*] " + str(volLength) + " volumes were found!")
                print("[~] Finding their Creation Dates...")
                a = i
                b = ri
            # SQLite Search Start
            cursor.execute('SELECT "{}" FROM "{}" WHERE Type="VOLUME" AND User=?'.format(a, b), (userSearch,))
            output = cursor.fetchall()
            del d[:]
            for row in output:
                d.append(str(row[0]))
            pos = 0
            for (row) in output:
                string1 = str(d[pos])
                pos = pos + 1
                # Volume Name List Start
                if counter == 0:
                    mount_volList.append(string1)
                    volLength = int = len(mount_volList)
                # Created Date List Start
                elif counter == 1:
                    mount_crList.append(string1)
                    crLength = int = len(mount_crList)
                else:
                    continue
            counter = counter + 1
        # Define variables for table
        elif (counter == 2) or (counter == 3):
            while y < volLength:
                # Define First Seen List Variables
                if counter == 2:
                    print("[~] Finding First Seen Date for Volume " + str(y) + "...")
                    a = icd
                    b = sls
                # Define Last Seen List Variables
                elif counter == 3:
                    print("[~] Finding Last Seen Date for Volume " + str(y) + "...")
                    a = du
                    b = sls
                else:
                    counter = counter + 1
                # SQLite Search Start
                cursor.execute('SELECT "{}" FROM "{}" WHERE kMDItemKind="Volume" AND kMDItemDisplayName =?'.format(a, b), (str(
                    mount_volList[y]),))
                output = cursor.fetchall()
                del e[:]
                for (row) in output:
                    e.append(str(row[0]))
                # First Seen List Start
                if counter == 2:
                    mount_fsList.append(str(e))
                    fsLength = int = len(mount_fsList)
                    if y == (volLength - 1):
                        y = 0
                        counter = counter + 1
                    else:
                        y = y + 1
                # Last Seen List Start
                elif counter == 3:
                    mount_lsList.append(str(e))
                    lsLength = int = len(mount_lsList)
                    if y == (volLength - 1):
                        y = 0
                        counter = counter + 1
                    else:
                        y = y + 1
                else:
                    y = (volLength + 1)
            # Get out of entire MAIN WHILE Loop
            end = "yes"

    # Define variables for output counting
    m = 0 # Counter for volLength
    z = 0 # List Position

    # Begin writing output
    # print("[#] Making all this data pretty...")
    while m < (volLength):
        file.write("\t-Volume Name: " + str(mount_volList[z]) + "\n" + "\t\tVolume created on: " + str(
            mount_crList[z]) + "\n" + "\t\tVolume first seen on: " + str(
            mount_fsList[z]) + "\n" + "\t\tVolume last seen on: " + str(
            mount_lsList[z]) + "\n")
        # Additional IF statement for identifying volumes present during forensic acquisition
        # This is based off the presence/absence of Spotlight Data values for each drive
        if str(mount_fsList[z]) == "[]":
            file.write('\t\t' + mount_volList[z] + ' was not imaged during forensic acquisition - possibly a secondary/removable device\n')
        else:
            file.write('\t\t' + mount_volList[z] + ' was imaged during forensic acquisition\n')
        m = m + 1
        z = z + 1

    # Global Variables
    a = "None"
    b = "None"
    output = None

    # mountedDevice.py variables
    x = mount_volList

    # Run Bash Session connections
    print("[#] Gathering relevant Bash Sessions...")
    print("[~] Finding Session Start Times...")
    print("[~] Finding Session End Times...")
    for row in x:
        L = 0
        # SQLite Search for Session Commands
        a = sc
        b = bs
        cursor.execute('SELECT "{}" FROM "{}" WHERE User = ? AND All_Commands LIKE ?'.format(a, b), (
            userSearch, '%' + str(x[L]) + '%',))
        bashOutput = cursor.fetchall()
        del e[:]
        for i in bashOutput:
            e.append(str(i[0]))
            pos = 0
            string1 = str(i[pos])
            pos = pos + 1
            mount_bashList.append(string1)
        L = L + 1
        L = 0
        
        # SQLite Search for Session Start
        a = ss
        b = bs
        cursor.execute('SELECT "{}" FROM "{}" WHERE User = ? AND All_Commands LIKE ?'.format(a, b), (
            userSearch, '%' + str(x[L]) + '%',))
        bashOutput = cursor.fetchall()
        del e[:]
        for i in bashOutput:
            e.append(str(i[0]))
            pos = 0
            string1 = str(i[pos])
            pos = pos + 1
            mount_ssList.append(string1)
        L = L + 1
        L = 0

        # SQLite Search for Session End
        a = se
        b = bs
        cursor.execute('SELECT "{}" FROM "{}" WHERE User = ? AND All_Commands LIKE ?'.format(a, b), (
            userSearch, '%' + str(x[L]) + '%',))
        bashOutput = cursor.fetchall()
        del e[:]
        for i in bashOutput:
            e.append(str(i[0]))
            pos = 0
            string1 = str(i[pos])
            pos = pos + 1
            mount_seList.append(string1)
        L = L + 1
        L = 0

    file.write("\t\t" + str(mount_bashList) + "\n")
    file.write("\t\t" + str(mount_ssList) + "\n")
    file.write("\t\t" + str(mount_seList) + "\n")

    # Show When Parsing Completed
    print("[*] Mounted Volume Parsing for " + user_name + " Completed!")
    # ------------------------------------------------

    # create temp json file
    filename = "tempmountedVolumes.json"

    JSON = {
        "user_name": user_name,
        "mount_volList": mount_volList,
        "mount_crList": mount_crList,
        "mount_fsList": mount_fsList,
        "mount_lsList": mount_lsList,
        "mount_bashList": mount_bashList,
        "mount_ssList": mount_ssList,
        "mount_seList": mount_seList
    }
    if filename:
        with open(filename, 'w') as f:
            json.dump(JSON, f)