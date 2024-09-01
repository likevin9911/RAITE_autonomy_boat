#!/usr/bin/env python3
import os
import re
import shutil

def find_and_manage_files():
    target_directory = '/home/sinloops/lidar-dc/Noisy_Images/'
    path = '.'  # Current directory, change if the files are in a different directory

    # Ensure target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created directory {target_directory}")

    # Find all files starting with 'dcl_' and ending with '.pcd'
    files = [f for f in os.listdir(path) if f.startswith('dcl_') and f.endswith('.pcd')]
    if not files:
        print("No files found.")
        return

    # Finding the largest file
    largest_file = max(files, key=lambda x: os.path.getsize(os.path.join(path, x)))

    # Delete other files
    for file in files:
        if file != largest_file:
            os.remove(os.path.join(path, file))
            #print(f"Deleted {file}")

    # Process the largest file name
    new_name = re.sub(r'\d{6,}', '', largest_file)  # Remove digits if there are more than 5 in a row

    # Move the file to the new directory
    src = os.path.join(path, largest_file)
    dst = os.path.join(target_directory, new_name)
    shutil.move(src, dst)
    print(f"Moved and renamed {largest_file} to {dst}")

if __name__ == '__main__':
    find_and_manage_files()
