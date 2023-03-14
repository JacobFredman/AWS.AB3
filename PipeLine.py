import os
import shutil
import boto3

# get the current working directory
current_dir = os.getcwd()

# set the path to the directoryToZip directory
GetBaseCryptoDataFolder = os.path.join(current_dir, 'GetBaseCryptoDataFolder')
directoryToZip = os.path.join(GetBaseCryptoDataFolder, 'CodeWithDependecies') 

# Set the name of the zip file you want to create
output_zip_filename = os.path.join(GetBaseCryptoDataFolder, 'GetBaseCrypoDataLambda') 

# Set the name of the S3 bucket you want to upload the zip file to
bucket_name = "crypto-data-f"

# Set the name of the CloudFormation stack you want to update
stack_name = "AB3Stack"

# Zip all the files in the directory
shutil.make_archive(output_zip_filename, 'zip', directoryToZip)
print("ziped seccesfuly")


# Upload the zip file to S3
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
with open(output_zip_filename + ".zip", "rb") as f:
    bucket.upload_fileobj(f, "GetBaseCrypoDataLambda" + ".zip")

print("uploaded to S3 seccesfuly")

# update the function with the new code
# AB3Stack-GetBaseCryptoDataFunction-5gbo2r0w8ShS
lambda_client = boto3.client('lambda')

response = lambda_client.update_function_code(
    FunctionName='AB3Stack-GetBaseCryptoDataFunction-5gbo2r0w8ShS',
    S3Bucket=bucket_name,
    S3Key='GetBaseCrypoDataLambda.zip'
)
print("Lambda updated")

# Update the CloudFormation stack with the new YAML template file
cloudformation = boto3.client('cloudformation')
with open("myTemplate.yaml", "r") as f:
    new_template_body = f.read()
cloudformation.update_stack(
    StackName=stack_name,
    TemplateBody=new_template_body,
    Capabilities=[
        'CAPABILITY_IAM'
    ]
)
print("updated stack seccefuly")

# command line to run the python file:
# /opt/homebrew/bin/python3 /Users/jfredmac/Desktop/Projects/AWS.AB3/pipeLine.py

