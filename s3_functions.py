import boto3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show_image(bucket):
    s3client = boto3.client("s3")
    public_urls = []
    try:
        logger.info(f"Attempting to list objects from bucket: {bucket}")
        response = s3client.list_objects(Bucket=bucket)
        
        if "Contents" not in response:
            logger.warning(f"No Contents key in response for bucket {bucket}. Response: {response}")
            return public_urls
            
        for item in response["Contents"]:
            presignedurl = s3client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": item["Key"]},
                ExpiresIn=1000,
            )
            public_urls.append(presignedurl)
            
        logger.info(f"Successfully retrieved {len(public_urls)} URLs from bucket {bucket}")
    except Exception as e:
        logger.error(f"Error accessing S3 bucket {bucket}: {str(e)}")
    
    return public_urls