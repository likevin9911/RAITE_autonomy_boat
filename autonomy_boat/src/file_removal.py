#!/usr/bin/env python3
import os

def delete_librealsense_file():
    # Define the file path
    file_path = '/home/lab/catkin_ws/devel/lib/librealsense2_camera.so'

    # Check if the file exists
    if os.path.isfile(file_path):
        try:
            # Delete the file
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
    else:
        print(f"File {file_path} not found.")

if __name__ == '__main__':
    delete_librealsense_file()

