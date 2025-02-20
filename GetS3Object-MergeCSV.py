import boto3
import botocore
import csv
import os


def download_file_with_resource(bucket_name, local_path):
    global new_file
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    files = my_bucket.objects.filter(Prefix='<BUCKET_DIRECTORY>/')
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
    path = r'<LOCAL_PATH>'
    main_file = r'<LOCAL_PATH>.csv'
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

bucket_name = '<BUCKET>'
local_path = '<LOCAL_PATH>'
download_file_with_resource(bucket_name, local_path)
append_csv()
