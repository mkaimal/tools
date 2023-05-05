#!/usr/local/bin/env python3 

import argparse
from wand.image import Image
import os 
import re
import multiprocessing as mp 


def filterPath(run_path):
    
    ''''
    this module helps to identify the running directory path and recurssive ones of directories and files that are of type png/jpg/jpeg
    '''
   
    # pool = mp.Pool(mp.cpu_count())
    for (root,dirs,files) in os.walk(run_path, topdown=True):
        #print(f'\nroot is : {root} \n\tdirs are {dirs} \n\t\tfiles are {files}')
        if files and [ pic_file for pic_file in files if pic_file.endswith(imageExtensions)]: 
            for file_name in files:
                if file_name.endswith(imageExtensions):
                    full_file_path = root +"/" + file_name
                    #print(f' Converting {full_file_path}')
                    # send the file path for thumbnail creation 
                    pool.apply_async(thumbNail(full_file_path))
            #ater all files are moved in single dir, send the dir path and file list for html creation 
            #print(f'Create index path at :{root,files}')
            pool.apply_async(indexHtml(root,files))
 
def indexHtml(dirPath,fileList):
    ifilePath = dirPath + "/" + "index.html" 
    print(f'Creating html file on : {ifilePath}')
    with open(ifilePath,'w') as inFile:
        inFile.write(f''' 
        <!DOCTYPE html>
        <html>
         ''')
        for ifileName in fileList:
        #print(f'at the path {dirPath} of ifileName is {ifileName}')
            if ifileName.endswith(imageExtensions):
                icoFile = re.sub('\.[A-Za-z]+$','_ico.png',ifileName)
                inFile.write(f'<a href="{ifileName}"><img src="{icoFile}"><a>')
        inFile.write(f'</html>')


            
def thumbNail(full_file_path):
    #print(f'thumbnailCreation:  {full_file_path}')
    ny = Image(filename = full_file_path)
    if ny.size > (80,60) : # comparing with size set , so same file is not take on a second run 
        ny.convert('png')
        ny.resize(80,60)
        newfilename = re.sub('\.[A-Za-z]+$','_ico.png',full_file_path)
        ny.save(filename = newfilename )

     


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(
        prog = "htmlcreatory.py",
        description="This script is designed to help create html files in directories",
        epilog="created by Mkaimal")
    
    parser.add_argument("-d", "--dir",
                        action='store',
                        dest='run_dir',
                        required='true',
                        help="Pass the full directory path for execution ")
    parser.add_argument("-v","--verbose",
                        action='store_true',
                        help="Debug on execution"    )

    args = parser.parse_args()
    system_paths = ('usr','sbin','root','bin', 'var')
    derive_base_path = args.run_dir.split('/')[1]
     # image extensions to consider for conversion 
    imageExtensions = ('.jpeg','.png', '.JPEG','.jpg','.JPG')

    if derive_base_path in system_paths: 
        print(f'Cannot execute in restricted root path')
    else: 
        print(f'<<< Executing on the directory : {args.run_dir} >>>')
        pool = mp.Pool(mp.cpu_count())
        filterPath(args.run_dir)



