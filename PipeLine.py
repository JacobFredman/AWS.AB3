import os
import boto3

# get the current working directory
current_dir = os.getcwd()

# set the path to the directoryToZip directory
GetBaseCryptoDataFolder = os.path.join(current_dir, 'GetBaseCryptoDataFolder')
directoryToZip = os.path.join(current_dir, 'CodeWithDependecies') 

# Set the name of the zip file you want to create
zipfile_name = "GetBaseCryptoDataFolder/GetBaseCrypoDataLambda.zip"

# Set the name of the S3 bucket you want to upload the zip file to
bucket_name = "crypto-data-general"

# Set the name of the CloudFormation stack you want to update
stack_name = "AB3Stack"

# Zip all the files in the directory
os.system(f"zip -r {zipfile_name} {directoryToZip}")

# Upload the zip file to S3
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
with open(zipfile_name, "rb") as f:
    bucket.upload_fileobj(f, zipfile_name)

# Update the CloudFormation stack with the new YAML template file
cloudformation = boto3.client('cloudformation')
with open("myTemplate.yaml", "r") as f:
    new_template_body = f.read()
cloudformation.update_stack(
    StackName=stack_name,
    TemplateBody=new_template_body
)
