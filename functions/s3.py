import boto3
import os
from datetime import datetime

from env.s3 import S3Settings
from env.cloudfront import CloudFrontSettings
from constants.constant import S3_DATE_FORMAT

settings = S3Settings()
cloudfront_settings = CloudFrontSettings()

class S3:

    def __init__(self) -> None:
        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = boto3.client('s3', 
                                       aws_access_key_id=settings.S3_AWS_ACCESS_KEY,
                                       aws_secret_access_key=settings.S3_AWS_SECRET_KEY,
                                       region_name=settings.S3_REGION)
            print("Connected to S3 Sucessfully !")
        except Exception as e:
            err_msg = f"S3 : Error connecting to S3 : {e}"
            print(err_msg)
            os._exit(0)

    def upload(self, binary, file_name, content_type, username):
        repo = settings.S3_REPO
        path_in_s3 = f'{repo}/{username}/{file_name}'
        try:
            response = self.client.put_object(Body=binary, Bucket=settings.S3_BUCKET, Key=path_in_s3, ContentType = content_type)
            print(f'S3 : Upload successful : {file_name}')

            upload_date_string = response["ResponseMetadata"]["HTTPHeaders"]["date"]
            uploaded_at = datetime.strptime(upload_date_string, S3_DATE_FORMAT)
            response = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.S3_BUCKET, "Key": path_in_s3},
                ExpiresIn=604800,
            )

            return False, f'{response}', uploaded_at
        except Exception as e:
            err_msg = f'S3 : Error Uploading : {e}'
            print(err_msg)
            return True, err_msg, None
            

