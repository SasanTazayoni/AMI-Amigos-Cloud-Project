import boto3
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

bucket_name = "se-data-with-ai-etl-project"

with open("test.txt", "w") as file:
    file.write("Testing boto3")

file_name = "test.txt"

s3_client.upload_file(
    Filename = file_name,
    Bucket = bucket_name,
    Key = "AMI-Amigos/" + file_name
)

print("Upload Successful")