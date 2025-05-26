import boto3
import logging
from botocore.config import Config
from botocore.exceptions import ClientError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_videos(bucket):
    s3_config = Config(signature_version='v4',
                       region_name='us-east-2',
                       s3={'addressing_style': 'virtual'})
    s3client = boto3.client("s3", config=s3_config)
    videos = []
    try:
        logger.info(f"Attempting to list objects from bucket: {bucket}")
        response = s3client.list_objects_v2(Bucket=bucket)

        if "Contents" not in response:
            logger.warning(
                f"No Contents key in response for bucket {bucket}. Response: {response}"
            )
            return videos

        for item in response["Contents"]:
            key = item["Key"]
            if key.lower().endswith((".mp4")):
                try:
                    head = s3client.head_object(Bucket=bucket, Key=key)
                    content_type = head.get("ContentType", "video/mp4")
                    size = head.get("ContentLength", 0)
                    last_modified = head.get("LastModified", 0)
                    presigned_url = s3client.generate_presigned_url(
                        "get_object",
                        Params={"Bucket": bucket, "Key": key},
                        ExpiresIn=7200,
                    )
                    data = head.get('Metadata', {})
                    title = key.split(".")[0]
                    videos.append({
                        "key": key,
                        "title": data['title'],
                        "artist": data['artist'],
                        "url": presigned_url,
                        "size": size,
                        "last_modified": last_modified,
                        "content_type": content_type
                    })
                except ClientError as e:
                    logger.error(f"Error getting metadata for {key}: {e}")
        logger.info(f"Successfully retrieved {len(videos)} URLs from bucket {bucket}")
    except Exception as e:
        logger.error(f"Error accessing S3 bucket {bucket}: {str(e)}")

    return videos
