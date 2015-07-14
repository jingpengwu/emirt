
import boto3

def upload_to_s3(fname, bucket_name, s3name):
    """
    upload file to s3 bucket
    """
    s3 = boto3.resource('s3')
    # Print out bucket names
    for bucket in s3.buckets.all():
        print(bucket.name)
    #s3.create_bucket(Bucket="znn")  
    s3.Object(bucket_name, s3name).put(Body=open(fname, 'rb'))
