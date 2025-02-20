import boto3
import botocore
import csv
import os, platform
import subprocess, sys

def download_file_with_resource(bucket_name, local_path):
    global new_file
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    files = my_bucket.objects.filter(Prefix='ise/')
    files = [obj.key for obj in sorted(files, key=lambda x: x.last_modified,
    reverse=True)][0:1]
    file = files[0]
    local_path += files[0].split("/",1)[1]
    
    print(file)
    print(local_path)
    new_file = local_path
    
    s3.Bucket(bucket_name).download_file(file, local_path)
    return(file)


def append_csv():
    path = r'C:\Users\mike.burns\Desktop\thorgroups\vpn configs\PowerBI\Data\RADIUSLogs'
    main_file = r'C:\Users\mike.burns\Desktop\thorgroups\vpn configs\PowerBI\Data\RADIUSLogs\RptExp_mburns.local_RADIUS_Authentications-Yesterday_2021-04-16_17-07-00.000000033.csv'
    #Find last modified file to merge
    files = list(os.scandir(path))
    track_created = 0
    for file in files:
        created = file.stat().st_mtime
        if created > track_created:
            track_created = created
            to_append = file
    check_out = os.path.isfile(main_file)
    #Open output file, creates if doesn't exist
    output = open(main_file,'a')
    file = open(to_append, 'r')
    if check_out:
        #Skip header and append content
        next(file)
        for line in file:
            output.write(line)
    else:
        #Append content
        for line in file:
            output.write(line)
    output.close()

def get_adusers(): 
    cmd = ["PowerShell", "-ExecutionPolicy", "Unrestricted", "-File", "C:\\Users\\mike.burns\\Desktop\\thorgroups\\vpn configs\\PowerBI\\Get-VPNGroupMembership.ps1"]  # Specify relative or absolute path to the script
    ec = subprocess.call(cmd)


def check_ping():
    hostname = "<ENTER HOSTNAME>"
    response = os.system("ping " + ("-n 1 " if  platform.system().lower()=="windows" else "-c 1 ") + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
        print(pingstatus, "- Script will continue")
        
        download_file_with_resource(bucket_name, local_path)

        append_csv()

        get_adusers()


    else:
        pingstatus = "Network Error"
        print(pingstatus, "- Script End. Please connect to VPN and re-run")

    #print(pingstatus)

bucket_name = '<ENTER BUCKET NAME>'
local_path = 'C:/Users/mike.burns/Desktop/thorgroups/vpn configs/PowerBI/Data/RADIUSLogs/'

check_ping()

