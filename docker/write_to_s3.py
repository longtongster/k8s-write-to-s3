import boto3

def write_to_s3():
    s3 = boto3.client('s3')
    bucket_name = "pytorch-svw"
    file_content = "Hello from boto3!"
    file_key = "boto3-test.txt"

    s3.put_object(Bucket=bucket_name, Key=file_key, Body=file_content)
    print(f"File {file_key} written to bucket {bucket_name}")

if __name__ == "__main__":
    write_to_s3()