#!/usr/bin/env python3
import os

# Set the directory path where your files are located
path = '/home/lab/catkin_ws/src/scripts/Noisy_Images'  # Replace with the path to your files

# A dictionary mapping the original numbers to the new numbers
rename_rules = {
    '100': '200',
    '300': '200',
    '500': '300',
    '700': '400',
    '900': '500',
    '1100': '600',
    '1300': '700',
    '1500': '800',
    '1700': '900',
    '1900': '1000',
    '2100': '1100',
    '2300': '1200',
    '2500': '1300',
    '2700': '1400',
}

# Function to rename the files based on the rules
def rename_files(directory, rules):
    for filename in os.listdir(directory):
        new_name = filename
        for old_number, new_number in rules.items():
            if old_number in filename:
                new_name = filename.replace(old_number, new_number)
                break  # Assuming only one number change per filename
        if new_name != filename:
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_name)
            os.rename(old_file, new_file)
            print(f'Renamed "{filename}" to "{new_name}"')

# Call the function to rename the files
rename_files(path, rename_rules)
