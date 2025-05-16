import boto3


def show_image(bucket):
    s3client = boto3.client("s3")
    public_urls = []
    try:
        for item in s3client.list_objects(Bucket=bucket)["Contents"]:
            presignedurl = s3client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": item["Key"]},
                ExpiresIn=1000,
            )
            public_urls.append(presignedurl)
    except Exception as e:
        pass
    return public_urls
