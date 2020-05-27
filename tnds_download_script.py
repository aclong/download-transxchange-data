#!/opt/anaconda/bin/python


#import libraries
from ftplib import FTP
import sys
import os
from datetime import datetime as dati
from pathlib import Path
from decouple import config

#get username and pass for trnasxchange from .env file need to register with traveline
user_name=config('USER_NAME')
pass_name=config('PASS_NAME')

#get time as string
now=dati.now()
date_string = now.strftime('%Y%m%d') 

#create destination folder name
dest_folder = f'/traveline_data/transxchange_download_region_date'

#connect to fts server
ftp=FTP(host = "ftp.tnds.basemap.co.uk", user=user_name, passwd=pass_name)

#get all filenames not including folders
file_names = []
ftp.retrlines('NLST', file_names.append)
file_ext_tup = (".zip", ".csv", ".txt")
file_names = [k for k in file_names if k.endswith(file_ext_tup)]

#download all files
for file in file_names:
    
    name_only = Path(file).stem    
    
    suffix = Path(file).suffix
    
    new_name = f'{name_only}_{date_string}{suffix}'
    
    with open(f'{dest_folder}/{new_name}', 'wb') as new_file:
        
        ftp.retrbinary('RETR %s' % f'{file}', new_file.write)
        
        new_file.close()

#quit ftp connection
ftp.quit()
