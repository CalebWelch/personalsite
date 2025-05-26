import boto3
from botocore.config import Config

s3_config = Config(signature_version='v4',
                       region_name='us-east-2',
                       s3={'addressing_style': 'virtual'})
s3Client = boto3.client("s3", config=s3_config)

BUCKET="visual-images"
s3Client.put_object(
    Bucket=BUCKET,
    Key="control.mp4",
    Metadata={
        "title": "Control",
        "artist": "Vier"
    }
)